
def test_duplicate_student(client):
    data = {
        "student_id": "DUP_ST001",
        "name": "Ankita",
        "age": 21,
        "email": "ankita@example.com",
        "department": "Computer Science"
    }

    first = client.post("/students", json=data)
    assert first.status_code == 200

    second = client.post("/students", json=data)
    assert second.status_code == 409


def test_invalid_student_email(client):
    data = {
        "student_id": "INVALID_ST001",
        "name": "Ankita",
        "age": 21,
        "email": "wrong-email",
        "department": "Computer Science"
    }

    response = client.post("/students", json=data)

    assert response.status_code == 422


def test_enrollment_with_missing_student(client):
    data = {
        "enrollment_id": "INVALID_EN001",
        "student_id": "NOT_FOUND_STUDENT",
        "course_code": "NOT_FOUND_COURSE"
    }

    response = client.post("/enrollments", json=data)

    assert response.status_code == 404


def test_enrollment_with_missing_course(client):
    # First create a valid student
    student = {
        "student_id": "VALID_ST001",
        "name": "Ankita",
        "age": 21,
        "email": "ankita@example.com",
        "department": "Computer Science"
    }

    client.post("/students", json=student)

    data = {
        "enrollment_id": "INVALID_EN002",
        "student_id": "VALID_ST001",
        "course_code": "NOT_FOUND_COURSE"
    }

    response = client.post("/enrollments", json=data)

    assert response.status_code == 404
