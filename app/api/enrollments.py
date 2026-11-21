
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database.models import Enrollment
from app.services.repository_enrollment_service import (
    add_enrollment as service_add_enrollment,
    get_enrollments as service_get_enrollments,
    update_enrollment as service_update_enrollment,
    delete_enrollment as service_delete_enrollment
)

router = APIRouter()


class EnrollmentData(BaseModel):
    enrollment_id: str
    student_id: str
    course_code: str


class EnrollmentUpdate(BaseModel):
    student_id: str
    course_code: str


@router.get("/enrollments")
def get_enrollments():
    enrollments = service_get_enrollments()

    return [
        {
            "enrollment_id": e.enrollment_id,
            "student_id": e.student_id,
            "course_code": e.course_code
        }
        for e in enrollments
    ]


@router.post("/enrollments")
def add_enrollment(data: EnrollmentData):

    enrollment = Enrollment(
        enrollment_id=data.enrollment_id,
        student_id=data.student_id,
        course_code=data.course_code
    )

    success, message = service_add_enrollment(enrollment)

    if not success:
        if message == "Enrollment ID already exists":
            raise HTTPException(status_code=409, detail=message)

        raise HTTPException(status_code=404, detail=message)

    return {
        "message": message,
        "enrollment_id": data.enrollment_id,
        "student_id": data.student_id,
        "course_code": data.course_code
    }


@router.put("/enrollments/{enrollment_id}")
def update_enrollment(enrollment_id: str, data: EnrollmentUpdate):

    success, message = service_update_enrollment(
        enrollment_id,
        data.student_id,
        data.course_code
    )

    if not success:
        raise HTTPException(status_code=404, detail=message)

    return {
        "message": message,
        "enrollment_id": enrollment_id,
        "student_id": data.student_id,
        "course_code": data.course_code
    }


@router.delete("/enrollments/{enrollment_id}")
def delete_enrollment(enrollment_id: str):

    success = service_delete_enrollment(enrollment_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    return {
        "message": "Enrollment deleted successfully",
        "enrollment_id": enrollment_id
    }
