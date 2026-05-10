from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.extension import _rate_limit_exceeded_handler
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import goit_hw_12.crud as crud
from goit_hw_12.auth import get_current_user, router as auth_router
from goit_hw_12.database import Base, engine, get_db
from goit_hw_12.models import User
from goit_hw_12.schemas import ContactCreate, ContactResponse, ContactUpdate
from goit_hw_12.users import router as users_router

Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Contacts REST API")

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


@app.post("/contacts/", response_model=ContactResponse, status_code=201)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return crud.create_contact(db, contact, current_user)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Contact with this email already exists",
        )


@app.get("/contacts/", response_model=List[ContactResponse])
def get_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.get_contacts(db, current_user)


@app.get("/contacts/search/", response_model=List[ContactResponse])
def search_contacts(
    query: str = Query(..., description="Search by first name, last name or email"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.search_contacts(db, query, current_user)


@app.get("/contacts/birthdays/", response_model=List[ContactResponse])
def get_upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.get_upcoming_birthdays(db, current_user)


@app.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = crud.get_contact(db, contact_id, current_user)

    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    return contact


@app.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_contact = crud.update_contact(
        db,
        contact_id,
        contact,
        current_user,
    )

    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    return updated_contact


@app.delete("/contacts/{contact_id}", response_model=ContactResponse)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted_contact = crud.delete_contact(db, contact_id, current_user)

    if deleted_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    return deleted_contact