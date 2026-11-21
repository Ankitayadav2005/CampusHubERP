
def test_student_crud(client):
    # Add student
    data = {
        "student_id": "TEST_ST001",
        "name": "Ankita",
        "age": 21,
        "email": "ankita_test@example.com",
        "department": "Computer Science"
    }

    response = client.post("/students", json=data)
    assert response.status_code == 200

    # Search student
    response = client.get("/students/TEST_ST001")
    assert response.status_code == 200
    assert response.json()["name"] == "Ankita"

    # Update student
    response = client.put(
        "/students/TEST_ST001",
        json={"name": "Ankita Updated"}
    )
    assert response.status_code == 200

    # Verify update
    response = client.get("/students/TEST_ST001")
    assert response.json()["name"] == "Ankita Updated"

    # Delete student
    response = client.delete("/students/TEST_ST001")
    assert response.status_code == 200

    # Verify deletion
    response = client.get("/students/TEST_ST001")
    assert response.status_code == 404


def test_faculty_crud(client):
    data = {
        "faculty_id": "TEST_FC001",
        "name": "Rahul",
        "age": 35,
        "email": "rahul_test@example.com",
        "department": "Computer Science"
    }

    response = client.post("/faculty", json=data)
    assert response.status_code == 200

    response = client.get("/faculty/TEST_FC001")
    assert response.status_code == 200
    assert response.json()["name"] == "Rahul"

    response = client.put(
        "/faculty/TEST_FC001",
        json={"name": "Rahul Updated"}
    )
    assert response.status_code == 200

    response = client.get("/faculty/TEST_FC001")
    assert response.json()["name"] == "Rahul Updated"

    response = client.delete("/faculty/TEST_FC001")
    assert response.status_code == 200

    response = client.get("/faculty/TEST_FC001")
    assert response.status_code == 404


def test_course_crud(client):
    data = {
        "course_code": "TEST_CS101",
        "course_name": "Python Programming",
        "credits": 4
    }

    response = client.post("/courses", json=data)
    assert response.status_code == 200

    response = client.get("/courses/TEST_CS101")
    assert response.status_code == 200
    assert response.json()["course_name"] == "Python Programming"

    response = client.put(
        "/courses/TEST_CS101",
        json={"course_name": "Advanced Python"}
    )
    assert response.status_code == 200

    response = client.get("/courses/TEST_CS101")
    assert response.json()["course_name"] == "Advanced Python"

    response = client.delete("/courses/TEST_CS101")
    assert response.status_code == 200

    response = client.get("/courses/TEST_CS101")
    assert response.status_code == 404



def test_enrollment_crud(client):

    # First create a student
    student_data = {
        "student_id": "TEST_ST001",
        "name": "Test Student",
        "age": 21,
        "email": "teststudent@example.com",
        "department": "Computer Science"
    }

    response = client.post("/students", json=student_data)
    assert response.status_code == 200

    # Then create a course
    course_data = {
        "course_code": "TEST_CS101",
        "course_name": "Test Python Course",
        "credits": 4
    }

    response = client.post("/courses", json=course_data)
    assert response.status_code == 200

    # Add enrollment
    enrollment_data = {
        "enrollment_id": "TEST_EN001",
        "student_id": "TEST_ST001",
        "course_code": "TEST_CS101"
    }

    response = client.post("/enrollments", json=enrollment_data)
    assert response.status_code == 200

    # Search enrollment
    response = client.get("/enrollments")
    assert response.status_code == 200

    enrollment_ids = [
        item["enrollment_id"] for item in response.json()
    ]
    assert "TEST_EN001" in enrollment_ids

    # Delete enrollment
    response = client.delete("/enrollments/TEST_EN001")
    assert response.status_code == 200

    # Verify deletion
    response = client.get("/enrollments")
    enrollment_ids = [
        item["enrollment_id"] for item in response.json()
    ]
    assert "TEST_EN001" not in enrollment_ids

def test_enrollment_update(client):

    # Create first student
    student1 = {
        "student_id": "UP_ST001",
        "name": "First Student",
        "age": 21,
        "email": "first@example.com",
        "department": "Computer Science"
    }

    response = client.post("/students", json=student1)
    assert response.status_code == 200

    # Create second student
    student2 = {
        "student_id": "UP_ST002",
        "name": "Second Student",
        "age": 22,
        "email": "second@example.com",
        "department": "IT"
    }

    response = client.post("/students", json=student2)
    assert response.status_code == 200

    # Create first course
    course1 = {
        "course_code": "UP_CS001",
        "course_name": "Python",
        "credits": 4
    }

    response = client.post("/courses", json=course1)
    assert response.status_code == 200

    # Create second course
    course2 = {
        "course_code": "UP_CS002",
        "course_name": "Database",
        "credits": 3
    }

    response = client.post("/courses", json=course2)
    assert response.status_code == 200

    # Create enrollment
    enrollment = {
        "enrollment_id": "UP_EN001",
        "student_id": "UP_ST001",
        "course_code": "UP_CS001"
    }

    response = client.post("/enrollments", json=enrollment)
    assert response.status_code == 200

    # Update enrollment
    updated_data = {
        "student_id": "UP_ST002",
        "course_code": "UP_CS002"
    }

    response = client.put(
        "/enrollments/UP_EN001",
        json=updated_data
    )

    assert response.status_code == 200

    # Verify updated enrollment
    response = client.get("/enrollments")
    assert response.status_code == 200

    updated_enrollment = next(
        item for item in response.json()
        if item["enrollment_id"] == "UP_EN001"
    )

    assert updated_enrollment["student_id"] == "UP_ST002"
    assert updated_enrollment["course_code"] == "UP_CS002"
