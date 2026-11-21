
from app.database import repository


def add_student(student):
    return repository.add_student(student)


def get_students():
    return repository.get_students()


def update_student(student_id, new_name):
    return repository.update_student(student_id, new_name)


def delete_student(student_id):
    return repository.delete_student(student_id)
