from fastapi.testclient import TestClient
from main import app, User, users_db

client = TestClient(app)


def test_create_user():
    user_json = {
        "username": "newer",
        "email": "newer@mail.com",
        "password": "111-22-33"
    }

    response = client.post("/users", json=user_json)

    assert response.status_code == 201

    response_json = response.json()
    assert response_json is not None
    assert response_json["id"] is not None
    del response_json["id"]
    assert response_json == user_json


def test_create_user_repeatedly():
    user_json = {
        "username": "double",
        "email": "double@mail.com",
        "password": "111-22-33"
    }

    response = client.post("/users/", json=user_json)
    assert response.status_code == 201

    response = client.post("/users/", json=user_json)
    assert response.status_code == 422


def test_create_user_missing_field():
    missing_json = {
        "username": "double",
        "email": "double@mail.com"
    }

    response = client.post("/users/", json=missing_json)
    assert response.status_code == 422


def test_get_user():
    id = 999999999
    user = User(id=id, username="Ivan",
                email="ivan@domen.org", password="999-99-00")
    users_db[id] = user

    response = client.get(f"users/{id}")

    assert response.status_code == 200
    assert response.json() == user.model_dump()

    del users_db[id]


def test_get_user_not_found():
    id = 999999991

    response = client.get(f"users/{id}")

    assert response.status_code == 404


def test_delete_user():
    id = 999999999
    user = User(id=id, username="Ivan",
                email="ivan@domen.org", password="999-99-00")
    users_db[id] = user

    response = client.delete(f"users/{id}")

    assert response.status_code == 204


def test_delete_user_not_fount():
    id = 999999991

    response = client.delete(f"users/{id}")

    assert response.status_code == 404
