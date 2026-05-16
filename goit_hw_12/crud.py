from datetime import date, timedelta

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from goit_hw_12.models import Contact, User
from goit_hw_12.schemas import ContactCreate, ContactUpdate


def create_contact(db: Session, contact: ContactCreate, user: User):
    """
    Create a new contact in the database.

    :param db: Database session.
    :param contact: Contact data to create.
    :param user: The user creating the contact.
    :return: The created contact.
    :raises IntegrityError: If the contact creation violates database constraints.
    """
    db_contact = Contact(
        **contact.model_dump(),
        user_id=user.id,
    )

    db.add(db_contact)

    try:
        db.commit()
        db.refresh(db_contact)
        return db_contact
    except IntegrityError:
        db.rollback()
        raise


def get_contacts(db: Session, user: User):
    """
    Retrieve all contacts for a specific user.

    :param db: Database session.
    :param user: The user whose contacts are to be retrieved.
    :return: A query object of the user's contacts.
    """
    return db.query(Contact).filter(Contact.user_id == user.id)


def get_contact(db: Session, contact_id: int, user: User):
    """
    Retrieve a specific contact by its ID for a specific user.

    :param db: Database session.
    :param contact_id: The ID of the contact to retrieve.
    :param user: The user who owns the contact.
    :return: The contact object if found, otherwise None.
    """
    return (
        db.query(Contact)
        .filter(Contact.id == contact_id)
        .filter(Contact.user_id == user.id)
        .first()
    )


def update_contact(
    db: Session,
    contact_id: int,
    contact: ContactUpdate,
    user: User,
):
    """
    Update a specific contact.

    :param db: Database session.
    :param contact_id: The ID of the contact to update.
    :param contact: The updated contact data.
    :param user: The user who owns the contact.
    :return: The updated contact object if found, otherwise None.
    """
    db_contact = get_contact(db, contact_id, user)

    if db_contact is None:
        return None

    for key, value in contact.model_dump(exclude_unset=True).items():
        setattr(db_contact, key, value)

    db.commit()
    db.refresh(db_contact)

    return db_contact


def delete_contact(db: Session, contact_id: int, user: User):
    """
    Delete a specific contact.

    :param db: Database session.
    :param contact_id: The ID of the contact to delete.
    :param user: The user who owns the contact.
    :return: The deleted contact object if found, otherwise None.
    """
    db_contact = get_contact(db, contact_id, user)

    if db_contact is None:
        return None

    db.delete(db_contact)
    db.commit()

    return db_contact


def search_contacts(db: Session, query: str, user: User):
    """
    Search for contacts by first name, last name, or email.

    :param db: Database session.
    :param query: The search query string.
    :param user: The user whose contacts are being searched.
    :return: A list of contacts matching the search query.
    """
    return (
        db.query(Contact)
        .filter(Contact.user_id == user.id)
        .filter(
            or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%"),
            )
        )
        .all()
    )


def get_upcoming_birthdays(db: Session, user: User):
    """
    Retrieve contacts with birthdays occurring in the next 7 days.

    :param db: Database session.
    :param user: The user whose contacts are to be checked.
    :return: A list of contacts with upcoming birthdays.
    """
    today = date.today()
    next_week = today + timedelta(days=7)

    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    result = []

    for contact in contacts:
        birthday_this_year = contact.birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = contact.birthday.replace(year=today.year + 1)

        if today <= birthday_this_year <= next_week:
            result.append(contact)

    return result
