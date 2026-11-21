from app.database.models import Student, Faculty, Course

from app.database.repository import (
    add_student,
    get_students,
    add_faculty,
    get_faculty,
    add_course,
    get_courses,
    update_student,
    delete_student,
    update_faculty,
    delete_faculty,
    update_course,
    delete_course
)


print("\n===== DATABASE TEST =====")


student = Student(
    student_id="ST001",
    name="Ankita",
    age=21,
    email="ankita@gmail.com",
    department="Computer Science"
)

add_student(student)


faculty = Faculty(
    faculty_id="FC001",
    name="Rahul",
    age=35,
    email="rahul@gmail.com",
    department="Computer Science"
)

add_faculty(faculty)


course = Course(
    course_code="CS101",
    course_name="Python Programming",
    credits=4
)

add_course(course)


print("\n===== STUDENTS =====")

for student in get_students():
    print(student.student_id, student.name)


print("\n===== FACULTY =====")

for faculty in get_faculty():
    print(faculty.faculty_id, faculty.name)


print("\n===== COURSES =====")

for course in get_courses():
    print(course.course_code, course.course_name)


print("\n===== FACULTY UPDATE TEST =====")

update_faculty("FC001", "Rahul Sharma")

for faculty in get_faculty():
    print(faculty.faculty_id, faculty.name)


print("\n===== COURSE UPDATE TEST =====")

update_course("CS101", "Advanced Python Programming")

for course in get_courses():
    print(course.course_code, course.course_name)