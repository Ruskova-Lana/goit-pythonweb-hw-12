from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.extension import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import goit_hw_12.crud as crud
from goit_hw_12.auth import get_current_user, router as auth_router
from goit_hw_12.database import Base, engine, get_db
from goit_hw_12.models import User
from goit_hw_12.schemas import ContactCreate, ContactResponse, ContactUpdate
from goit_hw_12.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.

    Creates database tables during application startup.
    The table creation is executed when the application starts,
    not during module import. This makes the application easier
    to import in tests and avoids unexpected database connections
    before the FastAPI app is initialized.
    """
    Base.metadata.create_all(bind=engine)
    yield


limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Contacts REST API",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(users_router)


@app.post(
    "/contacts/",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new contact for the authenticated user.

    :param contact: Contact data provided in request body.
    :param db: Database session.
    :param current_user: Authenticated user from JWT token.
    :return: Created contact.
    :raises HTTPException: 409 Conflict if contact email already exists.
    """
    try:
        return crud.create_contact(db, contact, current_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Contact with this email already exists",
        )


@app.get("/contacts/", response_model=List[ContactResponse])
def get_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all contacts that belong to the authenticated user.

    :param db: Database session.
    :param current_user: Authenticated user from JWT token.
    :return: List of user's contacts.
    """
    return crud.get_contacts(db, current_user)


@app.get("/contacts/search/", response_model=List[ContactResponse])
def search_contacts(
    query: str = Query(..., description="Search by first name, last name or email"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Search authenticated user's contacts by first name, last name or email.

    :param query: Search query string.
    :param db: Database session.
    :param current_user: Authenticated user from JWT token.
    :return: List of matching contacts.
    """
    return crud.search_contacts(db, query, current_user)


@app.get("/contacts/birthdays/", response_model=List[ContactResponse])
def get_upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get contacts with birthdays within the next 7 days.

    The query is limited to contacts that belong to the authenticated user.

    :param db: Database session.
    :param current_user: Authenticated user from JWT token.
    :return: List of contacts with upcoming birthdays.
    """
    return crud.get_upcoming_birthdays(db, current_user)


@app.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a single contact by ID.

    The contact must belong to the authenticated user.

    :param contact_id: Contact identifier.
    :param db: Database session.
    :param current_user: Authenticated user from JWT token.
    :return: Contact object.
    :raises HTTPException: 404 Not Found if contact does not exist.
    """
    contact = crud.get_contact(db, contact_id, current_user)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )

    return contact


@app.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update an existing contact.

    The contact must belong to the authenticated user.

    :param contact_id: Contact identifier.
    :param contact: Updated contact data.
    :param db: Database session.
    :param current_user: Authenticated user from JWT token.
    :return: Updated contact.
    :raises HTTPException: 404 Not Found if contact does not exist.
    """
    updated_contact = crud.update_contact(
        db=db,
        contact_id=contact_id,
        contact=contact,
        user=current_user,
    )

    if updated_contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )

    return updated_contact


@app.delete("/contacts/{contact_id}", response_model=ContactResponse)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete an existing contact.

    The contact must belong to the authenticated user.

    :param contact_id: Contact identifier.
    :param db: Database session.
    :param current_user: Authenticated user from JWT token.
    :return: Deleted contact.
    :raises HTTPException: 404 Not Found if contact does not exist.
    """
    deleted_contact = crud.delete_contact(
        db=db,
        contact_id=contact_id,
        user=current_user,
    )

    if deleted_contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )

    return deleted_contact