from fastapi import status
from fastapi.testclient import TestClient

from app.main import app, Contact, contacts_db

client = TestClient(app)


def test_create_contact():
    contact_json = {
        "name": "newer",
        "email": "newer@mail.com",
        "phone": "111-22-33"
    }

    response = client.post("/contacts/", json=contact_json)

    assert response.status_code == status.HTTP_201_CREATED

    response_json = response.json()
    assert response_json is not None
    del response_json["id"]
    assert response_json == contact_json


def test_create_contact_repeatedly():
    contact_json = {
        "name": "double",
        "email": "double@mail.com",
        "phone": "111-22-33"
    }

    response = client.post("/contacts/", json=contact_json)
    assert response.status_code == status.HTTP_201_CREATED

    response = client.post("/contacts/", json=contact_json)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_contact_missing_field():
    missing_json = {
        "name": "double",
        "email": "double@mail.com"
    }

    response = client.post("/contacts/", json=missing_json)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_contact():
    id = 999999999
    contact = Contact(id=id, name="Ivan",
                      email="ivan@domen.org", phone="999-99-00")
    contacts_db[id] = contact

    response = client.get(f"contacts/{id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == contact.model_dump()

    del contacts_db[id]


def test_get_contact_not_found():
    id = 999999991

    response = client.get(f"contacts/{id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_contact():
    id = 999999999
    contact = Contact(id=id, name="Ivan",
                      email="ivan@domen.org", phone="999-99-00")
    contacts_db[id] = contact

    response = client.delete(f"contacts/{id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_contact_not_fount():
    id = 999999991

    response = client.delete(f"contacts/{id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
