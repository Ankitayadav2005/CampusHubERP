
from sqlalchemy import Column, Integer, String
from app.database.db import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    student_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer)
    email = Column(String)
    department = Column(String)


class Faculty(Base):
    __tablename__ = "faculty"

    id = Column(Integer, primary_key=True)
    faculty_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer)
    email = Column(String)
    department = Column(String)


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    course_code = Column(String, unique=True, nullable=False)
    course_name = Column(String, nullable=False)
    credits = Column(Integer)


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True)
    enrollment_id = Column(String, unique=True, nullable=False)
    student_id = Column(String, nullable=False)
    course_code = Column(String, nullable=False)
