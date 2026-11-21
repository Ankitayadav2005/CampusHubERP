
from app.database import repository


def add_faculty(faculty):
    return repository.add_faculty(faculty)


def get_faculty():
    return repository.get_faculty()


def update_faculty(faculty_id, new_name):
    return repository.update_faculty(faculty_id, new_name)


def delete_faculty(faculty_id):
    return repository.delete_faculty(faculty_id)
