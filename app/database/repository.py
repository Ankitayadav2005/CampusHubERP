
from app.database.db import SessionLocal
from app.database.models import Student, Faculty, Course, Enrollment
from app.core.logger import logger


# ---------------- STUDENT ----------------

def add_student(student):
    db = SessionLocal()
    try:
        existing = db.query(Student).filter(
            Student.student_id == student.student_id
        ).first()

        if existing:
            logger.warning(
                "Student already exists: %s", student.student_id
            )
            return False

        db.add(student)
        db.commit()

        logger.info("Student added: %s", student.student_id)
        return True

    except Exception:
        db.rollback()
        logger.exception("Error adding student: %s", student.student_id)
        return False

    finally:
        db.close()


def get_students():
    db = SessionLocal()
    try:
        students = db.query(Student).all()
        logger.info("Retrieved %s students", len(students))
        return students
    except Exception:
        logger.exception("Error retrieving students")
        raise
    finally:
        db.close()


def update_student(student_id, new_name):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(
            Student.student_id == student_id
        ).first()

        if student:
            student.name = new_name
            db.commit()
            logger.info("Student updated: %s", student_id)
            return True

        logger.warning("Student not found for update: %s", student_id)
        return False

    except Exception:
        db.rollback()
        logger.exception("Error updating student: %s", student_id)
        raise
    finally:
        db.close()


def delete_student(student_id):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(
            Student.student_id == student_id
        ).first()

        if student:
            db.delete(student)
            db.commit()
            logger.info("Student deleted: %s", student_id)
            return True

        logger.warning("Student not found for deletion: %s", student_id)
        return False

    except Exception:
        db.rollback()
        logger.exception("Error deleting student: %s", student_id)
        raise
    finally:
        db.close()


# ---------------- FACULTY ----------------

def add_faculty(faculty):
    db = SessionLocal()
    try:
        db.add(faculty)
        db.commit()
        logger.info("Faculty added: %s", faculty.faculty_id)

    except Exception:
        db.rollback()
        logger.exception("Error adding faculty")
        raise

    finally:
        db.close()


def get_faculty():
    db = SessionLocal()
    try:
        faculty = db.query(Faculty).all()
        logger.info("Retrieved %s faculty records", len(faculty))
        return faculty
    except Exception:
        logger.exception("Error retrieving faculty")
        raise
    finally:
        db.close()


def update_faculty(faculty_id, new_name):
    db = SessionLocal()
    try:
        faculty = db.query(Faculty).filter(
            Faculty.faculty_id == faculty_id
        ).first()

        if faculty:
            faculty.name = new_name
            db.commit()
            logger.info("Faculty updated: %s", faculty_id)
            return True

        logger.warning("Faculty not found for update: %s", faculty_id)
        return False

    except Exception:
        db.rollback()
        logger.exception("Error updating faculty: %s", faculty_id)
        raise
    finally:
        db.close()


def delete_faculty(faculty_id):
    db = SessionLocal()
    try:
        faculty = db.query(Faculty).filter(
            Faculty.faculty_id == faculty_id
        ).first()

        if faculty:
            db.delete(faculty)
            db.commit()
            logger.info("Faculty deleted: %s", faculty_id)
            return True

        logger.warning("Faculty not found for deletion: %s", faculty_id)
        return False

    except Exception:
        db.rollback()
        logger.exception("Error deleting faculty: %s", faculty_id)
        raise
    finally:
        db.close()


# ---------------- COURSE ----------------

def add_course(course):
    db = SessionLocal()
    try:
        db.add(course)
        db.commit()
        logger.info("Course added: %s", course.course_code)

    except Exception:
        db.rollback()
        logger.exception("Error adding course")
        raise

    finally:
        db.close()


def get_courses():
    db = SessionLocal()
    try:
        courses = db.query(Course).all()
        logger.info("Retrieved %s courses", len(courses))
        return courses
    except Exception:
        logger.exception("Error retrieving courses")
        raise
    finally:
        db.close()


def update_course(course_code, new_name):
    db = SessionLocal()
    try:
        course = db.query(Course).filter(
            Course.course_code == course_code
        ).first()

        if course:
            course.course_name = new_name
            db.commit()
            logger.info("Course updated: %s", course_code)
            return True

        logger.warning("Course not found for update: %s", course_code)
        return False

    except Exception:
        db.rollback()
        logger.exception("Error updating course: %s", course_code)
        raise
    finally:
        db.close()


def delete_course(course_code):
    db = SessionLocal()
    try:
        course = db.query(Course).filter(
            Course.course_code == course_code
        ).first()

        if course:
            db.delete(course)
            db.commit()
            logger.info("Course deleted: %s", course_code)
            return True

        logger.warning("Course not found for deletion: %s", course_code)
        return False

    except Exception:
        db.rollback()
        logger.exception("Error deleting course: %s", course_code)
        raise
    finally:
        db.close()


# ---------------- ENROLLMENT ----------------

def add_enrollment(enrollment):
    db = SessionLocal()
    try:
        existing = db.query(Enrollment).filter(
            Enrollment.enrollment_id == enrollment.enrollment_id
        ).first()

        if existing:
            logger.warning(
                "Enrollment ID already exists: %s",
                enrollment.enrollment_id
            )
            return False, "Enrollment ID already exists"

        student = db.query(Student).filter(
            Student.student_id == enrollment.student_id
        ).first()

        if student is None:
            logger.warning(
                "Student not found for enrollment: %s",
                enrollment.student_id
            )
            return False, "Student not found"

        course = db.query(Course).filter(
            Course.course_code == enrollment.course_code
        ).first()

        if course is None:
            logger.warning(
                "Course not found for enrollment: %s",
                enrollment.course_code
            )
            return False, "Course not found"

        db.add(enrollment)
        db.commit()

        logger.info(
            "Enrollment added: %s",
            enrollment.enrollment_id
        )
        return True, "Enrollment added successfully"

    except Exception:
        db.rollback()
        logger.exception("Error adding enrollment")
        raise

    finally:
        db.close()


def get_enrollments():
    db = SessionLocal()
    try:
        enrollments = db.query(Enrollment).all()
        logger.info("Retrieved %s enrollments", len(enrollments))
        return enrollments
    except Exception:
        logger.exception("Error retrieving enrollments")
        raise
    finally:
        db.close()


def update_enrollment(enrollment_id, new_student_id, new_course_code):
    db = SessionLocal()
    try:
        enrollment = db.query(Enrollment).filter(
            Enrollment.enrollment_id == enrollment_id
        ).first()

        if enrollment is None:
            logger.warning("Enrollment not found: %s", enrollment_id)
            return False, "Enrollment not found"

        student = db.query(Student).filter(
            Student.student_id == new_student_id
        ).first()

        if student is None:
            logger.warning("Student not found: %s", new_student_id)
            return False, "Student not found"

        course = db.query(Course).filter(
            Course.course_code == new_course_code
        ).first()

        if course is None:
            logger.warning("Course not found: %s", new_course_code)
            return False, "Course not found"

        enrollment.student_id = new_student_id
        enrollment.course_code = new_course_code

        db.commit()

        logger.info("Enrollment updated: %s", enrollment_id)
        return True, "Enrollment updated successfully"

    except Exception:
        db.rollback()
        logger.exception("Error updating enrollment: %s", enrollment_id)
        raise

    finally:
        db.close()


def delete_enrollment(enrollment_id):
    db = SessionLocal()
    try:
        enrollment = db.query(Enrollment).filter(
            Enrollment.enrollment_id == enrollment_id
        ).first()

        if enrollment is None:
            logger.warning("Enrollment not found for deletion: %s", enrollment_id)
            return False

        db.delete(enrollment)
        db.commit()

        logger.info("Enrollment deleted: %s", enrollment_id)
        return True

    except Exception:
        db.rollback()
        logger.exception("Error deleting enrollment: %s", enrollment_id)
        raise

    finally:
        db.close()
