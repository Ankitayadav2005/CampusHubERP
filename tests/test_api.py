
def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "CampusHub ERP" in response.text


def test_get_students(client):
    response = client.get("/students")
    assert response.status_code == 200


def test_get_faculty(client):
    response = client.get("/faculty")
    assert response.status_code == 200


def test_get_courses(client):
    response = client.get("/courses")
    assert response.status_code == 200


def test_get_enrollments(client):
    response = client.get("/enrollments")
    assert response.status_code == 200
