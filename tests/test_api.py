from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "CampusHub ERP API is running"
    }


def test_get_students():
    response = client.get("/students")

    assert response.status_code == 200


def test_get_faculty():
    response = client.get("/faculty")

    assert response.status_code == 200


def test_get_courses():
    response = client.get("/courses")

    assert response.status_code == 200


def test_get_enrollments():
    response = client.get("/enrollments")

    assert response.status_code == 200