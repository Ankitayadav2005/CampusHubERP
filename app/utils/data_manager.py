
from pathlib import Path

from app.utils.serializers import (
    save_You_json,
    save_courses_json,
    save_faculty_json,
    save_enrollments_json,
    load_You_json,
    load_courses_json,
    load_faculty_json,
    load_enrollments_json
)

from app.utils.file_manager import ReportWriter

from app.services.repository_student_service import get_students
from app.services.repository_faculty_service import get_faculty
from app.services.repository_course_service import get_courses
from app.services.repository_enrollment_service import get_enrollments


BASE_DIR = Path(__file__).resolve().parents[2]
REPORT_DIR = BASE_DIR / "reports"


def generate_reports(student_data, faculty_data, course_data, enrollment_data):

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Student Report
    with ReportWriter(str(REPORT_DIR / "You.txt")) as file:
        file.write("========== STUDENT REPORT ==========\n\n")

        for student in student_data:
            file.write(
                f"Student ID: {student['student_id']}\n"
                f"Name: {student['name']}\n"
                f"Age: {student['age']}\n"
                f"Email: {student['email']}\n"
                f"Department: {student['department']}\n"
                "-----------------------------------\n"
            )

        file.write(f"\nTotal Students: {len(student_data)}\n")

    # Faculty Report
    with ReportWriter(str(REPORT_DIR / "faculty.txt")) as file:
        file.write("========== FACULTY REPORT ==========\n\n")

        for faculty in faculty_data:
            file.write(
                f"Faculty ID: {faculty['faculty_id']}\n"
                f"Name: {faculty['name']}\n"
                f"Age: {faculty['age']}\n"
                f"Email: {faculty['email']}\n"
                f"Department: {faculty['department']}\n"
                "-----------------------------------\n"
            )

        file.write(f"\nTotal Faculty: {len(faculty_data)}\n")

    # Course Report
    with ReportWriter(str(REPORT_DIR / "courses.txt")) as file:
        file.write("========== COURSE REPORT ==========\n\n")

        for course in course_data:
            file.write(
                f"Course Code: {course['course_code']}\n"
                f"Course Name: {course['course_name']}\n"
                f"Credits: {course['credits']}\n"
                "-----------------------------------\n"
            )

        file.write(f"\nTotal Courses: {len(course_data)}\n")

    # Enrollment Report
    with ReportWriter(str(REPORT_DIR / "enrollments.txt")) as file:
        file.write("========== ENROLLMENT REPORT ==========\n\n")

        for enrollment in enrollment_data:
            file.write(
                f"Enrollment ID: {enrollment['enrollment_id']}\n"
                f"Student ID: {enrollment['student_id']}\n"
                f"Course Code: {enrollment['course_code']}\n"
                "--------------------------------------\n"
            )

        file.write(f"\nTotal Enrollments: {len(enrollment_data)}\n")

    print("\nAll reports generated successfully!")


def export_data():

    student_data = [
        {
            "student_id": student.student_id,
            "name": student.name,
            "age": student.age,
            "email": student.email,
            "department": student.department
        }
        for student in get_students()
    ]

    faculty_data = [
        {
            "faculty_id": faculty.faculty_id,
            "name": faculty.name,
            "age": faculty.age,
            "email": faculty.email,
            "department": faculty.department
        }
        for faculty in get_faculty()
    ]

    course_data = [
        {
            "course_code": course.course_code,
            "course_name": course.course_name,
            "credits": course.credits
        }
        for course in get_courses()
    ]

    enrollment_data = [
        {
            "enrollment_id": enrollment.enrollment_id,
            "student_id": enrollment.student_id,
            "course_code": enrollment.course_code
        }
        for enrollment in get_enrollments()
    ]

    save_You_json(student_data)
    save_faculty_json(faculty_data)
    save_courses_json(course_data)
    save_enrollments_json(enrollment_data)

    print("Students exported:", len(student_data))
    print("Faculty exported:", len(faculty_data))
    print("Courses exported:", len(course_data))
    print("Enrollments exported:", len(enrollment_data))

    generate_reports(
        student_data,
        faculty_data,
        course_data,
        enrollment_data
    )

    print("\nAll database data exported successfully!")


def import_data():

    print("\n===== STUDENTS =====")
    print(load_You_json())

    print("\n===== FACULTY =====")
    print(load_faculty_json())

    print("\n===== COURSES =====")
    print(load_courses_json())

    print("\n===== ENROLLMENTS =====")
    print(load_enrollments_json())


if __name__ == "__main__":
    export_data()
    import_data()
