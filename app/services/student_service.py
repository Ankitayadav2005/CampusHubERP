
from app.utils.decorators import log_decorator, time_decorator


students = []


@log_decorator
@time_decorator
def add_student(student):
    students.append(student)
    print("Student added successfully.")


@log_decorator
@time_decorator
def remove_student(student_id):
    for student in students:
        if student.student_id == student_id:
            students.remove(student)
            print("Student removed successfully.")
            return

    print("Student not found.")


@log_decorator
@time_decorator
def update_student(
    student_id,
    name=None,
    age=None,
    email=None,
    department=None
):
    for student in students:
        if student.student_id == student_id:

            if name is not None:
                student.name = name

            if age is not None:
                student.age = age

            if email is not None:
                student.email = email

            if department is not None:
                student.department = department

            print("Student updated successfully.")
            return

    print("Student not found.")


@log_decorator
@time_decorator
def list_students():
    return students


def list_students_uppercase():
    return list(
        map(
            lambda student: student.name.upper(),
            students
        )
    )


def filter_students_by_department(department):
    return list(
        filter(
            lambda student: student.department == department,
            students
        )
    )


def sort_students_by_name():
    return sorted(
        students,
        key=lambda student: student.name
    )