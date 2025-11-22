import requests
from jsonschema import validate
from resources.schemas import post_create_user, put_update_user, invalid_register, valid_register

# 1. GET + 200

BASE_URL = "https://reqres.in/api"

def test_get_users():
    response = requests.get(f"{BASE_URL}/users?page=2")
    body = response.json()

    assert response.status_code == 200
    assert len(body["data"]) > 0

# 2. POST + 201

def test_post_create_user():
    response = requests.post(
        f"{BASE_URL}/users",
        headers={"x-api-key": "reqres-free-v1"},
        json={"name": "morpheus", "job": "leader"})
    body = response.json()

    assert response.status_code == 201
    validate(body, schema=post_create_user)

# 3. PUT

def test_put_update_user():
    response = requests.put(
        f"{BASE_URL}/users/2",
        headers={"x-api-key": "reqres-free-v1"},
        json={"name": "neo", "job": "specialone"}
    )
    body = response.json()

    validate(body, schema=put_update_user)


# 4. DELETE + 204

def test_delete_user():
    response = requests.delete(
        f"{BASE_URL}/users/2",
        headers={"x-api-key": "reqres-free-v1"}
    )

    assert response.status_code == 204


# Positive with response body

def test_success_register():
    response = requests.post(
        f"{BASE_URL}/register",
        headers={"x-api-key": "reqres-free-v1"},
        json={"email": "eve.holt@reqres.in","password": "pistol"}
    )

    body = response.json()

    validate(body, valid_register)
    assert body["id"] == 4
    assert body["token"] == "QpwL5tke4Pnpja7X4"

# Negative + 400

def test_register_missing_password():
    response = requests.post(
        f"{BASE_URL}/register",
        headers={"x-api-key": "reqres-free-v1"},
        json={"email": "sydney@fife", "password": ""}
    )

    body = response.json()

    assert response.status_code == 400
    validate(body, invalid_register)
    assert response.json()["error"] == "Missing password"

# 404 w/o response body

def test_not_found():
    response = requests.get(f"{BASE_URL}/api/unknown/23", headers={"x-api-key": "reqres-free-v1"},)
    body = response.json()

    assert response.status_code == 404
    assert body == {}

