from datetime import date, timedelta 
from unittest.mock import MagicMock

from goit_hw_12.crud import (
    create_contact,
    delete_contact,
    get_contact,
    get_contacts,
    update_contact,
    get_upcoming_birthdays,
    get_upcoming_birthdays,
    
)
from goit_hw_12.models import Contact
from goit_hw_12.schemas import ContactUpdate, ContactCreate


def test_get_contacts():
    db = MagicMock()
    user = MagicMock()
    user.id = 1

    result = get_contacts(db=db, user=user)

    assert result is not None

def test_create_contact():
    db = MagicMock()
    user = MagicMock()
    user.id = 1

    contact = ContactCreate(
        first_name="Ruslana",
        last_name="Test",
        email="ruslana@test.com",
        phone="123456789",
        birthday=date(1990, 5, 10),
        additional_info="test",
    )

    result = create_contact(
        db=db,
        contact=contact,
        user=user,
    )

    assert result.first_name == "Ruslana"
    assert result.user_id == 1

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_get_contact_not_found():
    db = MagicMock()
    user = MagicMock()
    user.id = 1

    db.query.return_value.filter.return_value.filter.return_value.first.return_value = None

    result = get_contact(db=db, contact_id=999, user=user)

    assert result is None


def test_update_contact_not_found():
    db = MagicMock()
    user = MagicMock()
    user.id = 1

    db.query.return_value.filter.return_value.filter.return_value.first.return_value = None

    update_data = ContactUpdate(
        first_name="New",
        last_name="Name",
        email="new@test.com",
        phone="222",
        birthday=date(1991, 2, 2),
        additional_info="updated",
    )

    result = update_contact(
        db=db,
        contact_id=999,
        contact=update_data,
        user=user,
    )

    assert result is None


def test_delete_contact_not_found():
    db = MagicMock()
    user = MagicMock()
    user.id = 1

    db.query.return_value.filter.return_value.filter.return_value.first.return_value = None

    result = delete_contact(db=db, contact_id=999, user=user)

    assert result is None


def test_get_upcoming_birthdays_empty():
    db = MagicMock()
    user = MagicMock()
    user.id = 1

    db.query.return_value.filter.return_value.all.return_value = []

    result = get_upcoming_birthdays(db=db, user=user)

    assert result == []


def test_get_upcoming_birthdays_future_in_7_days():
    db = MagicMock()
    user = MagicMock()
    user.id = 1

    future_birthday = date.today() + timedelta(days=5)

    contact = Contact(
        id=1,
        first_name="Future",
        last_name="Birthday",
        email="future@test.com",
        phone="123",
        birthday=future_birthday,
        user_id=1,
    )

    db.query.return_value.filter.return_value.all.return_value = [contact]

    result = get_upcoming_birthdays(db=db, user=user)

    assert len(result) == 1