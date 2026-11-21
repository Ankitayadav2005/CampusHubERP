
import re

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator

from app.database.models import Student
from app.database.repository import (
    add_student as db_add_student,
    get_students as db_get_students,
    update_student as db_update_student,
    delete_student as db_delete_student
)

router = APIRouter()


class StudentData(BaseModel):
    student_id: str
    name: str
    age: int
    email: str
    department: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.match(pattern, value):
            raise ValueError("Invalid email address")

        return value


class StudentUpdate(BaseModel):
    name: str


@router.get("/students")
def get_students():
    students = db_get_students()

    return [
        {
            "student_id": s.student_id,
            "name": s.name,
            "age": s.age,
            "email": s.email,
            "department": s.department
        }
        for s in students
    ]


@router.post("/students")
def create_student(data: StudentData):
    student = Student(
        student_id=data.student_id,
        name=data.name,
        age=data.age,
        email=data.email,
        department=data.department
    )

    result = db_add_student(student)

    if not result:
        raise HTTPException(
            status_code=409,
            detail="Student ID already exists"
        )

    return {
        "message": "Student added successfully",
        "student_id": data.student_id
    }


@router.get("/students/{student_id}")
def get_student(student_id: str):
    students = db_get_students()

    for s in students:
        if s.student_id == student_id:
            return {
                "student_id": s.student_id,
                "name": s.name,
                "age": s.age,
                "email": s.email,
                "department": s.department
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


@router.put("/students/{student_id}")
def update_student(student_id: str, data: StudentUpdate):
    success = db_update_student(student_id, data.name)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student updated successfully",
        "student_id": student_id
    }


@router.delete("/students/{student_id}")
def delete_student(student_id: str):
    success = db_delete_student(student_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student deleted successfully",
        "student_id": student_id
    }
