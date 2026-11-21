
from app.utils.decorators import log_decorator, time_decorator


faculties = []


@log_decorator
@time_decorator
def add_faculty(faculty):
    faculties.append(faculty)
    print("Faculty added successfully.")


@log_decorator
@time_decorator
def remove_faculty(faculty_id):
    for faculty in faculties:
        if faculty.faculty_id == faculty_id:
            faculties.remove(faculty)
            print("Faculty removed successfully.")
            return

    print("Faculty not found.")


@log_decorator
@time_decorator
def update_faculty(
    faculty_id,
    name=None,
    age=None,
    email=None,
    department=None
):
    for faculty in faculties:
        if faculty.faculty_id == faculty_id:

            if name is not None:
                faculty.name = name

            if age is not None:
                faculty.age = age

            if email is not None:
                faculty.email = email

            if department is not None:
                faculty.department = department

            print("Faculty updated successfully.")
            return

    print("Faculty not found.")


@log_decorator
@time_decorator
def list_faculty():
    return faculties


def list_faculty_uppercase():
    return list(
        map(
            lambda faculty: faculty.name.upper(),
            faculties
        )
    )


def filter_faculty_by_department(department):
    return list(
        filter(
            lambda faculty: faculty.department == department,
            faculties
        )
    )


def sort_faculty_by_name():
    return sorted(
        faculties,
        key=lambda faculty: faculty.name
    )