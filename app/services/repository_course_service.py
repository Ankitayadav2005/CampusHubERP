
from app.database import repository


def add_course(course):
    return repository.add_course(course)


def get_courses():
    return repository.get_courses()


def update_course(course_code, new_name):
    return repository.update_course(course_code, new_name)


def delete_course(course_code):
    return repository.delete_course(course_code)
