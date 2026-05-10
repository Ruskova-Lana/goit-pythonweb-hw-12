from datetime import date, timedelta

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from goit_hw_12.models import Contact, User
from goit_hw_12.schemas import ContactCreate, ContactUpdate


def create_contact(db: Session, contact: ContactCreate, user: User):
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
    return db.query(Contact).filter(Contact.user_id == user.id)


def get_contact(db: Session, contact_id: int, user: User):
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
    db_contact = get_contact(db, contact_id, user)

    if db_contact is None:
        return None

    for key, value in contact.model_dump(exclude_unset=True).items():
        setattr(db_contact, key, value)

    db.commit()
    db.refresh(db_contact)

    return db_contact


def delete_contact(db: Session, contact_id: int, user: User):
    db_contact = get_contact(db, contact_id, user)

    if db_contact is None:
        return None

    db.delete(db_contact)
    db.commit()

    return db_contact


def search_contacts(db: Session, query: str, user: User):
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
