
from app.database import repository


def add_enrollment(enrollment):
    return repository.add_enrollment(enrollment)


def get_enrollments():
    return repository.get_enrollments()


def delete_enrollment(enrollment_id):
    return repository.delete_enrollment(enrollment_id)

def update_enrollment(enrollment_id, new_student_id, new_course_code):
    return repository.update_enrollment(
        enrollment_id,
        new_student_id,
        new_course_code
    )

def update_enrollment(enrollment_id, new_student_id, new_course_code):
    return repository.update_enrollment(
        enrollment_id,
        new_student_id,
        new_course_code
    )
