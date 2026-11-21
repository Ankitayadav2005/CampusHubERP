from app.models.enrollment import Enrollment


enrollments = []


def add_enrollment(enrollment):
    enrollments.append(enrollment)
    print("Enrollment added successfully.")


def remove_enrollment(enrollment_id):
    for enrollment in enrollments:
        if enrollment.enrollment_id == enrollment_id:
            enrollments.remove(enrollment)
            print("Enrollment removed successfully.")
            return

    print("Enrollment not found.")


def list_enrollments():
    return enrollments