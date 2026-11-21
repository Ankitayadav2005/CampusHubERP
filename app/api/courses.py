
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database.models import Course
from app.services.repository_course_service import (
    add_course as service_add_course,
    get_courses as service_get_courses,
    update_course as service_update_course,
    delete_course as service_delete_course
)

router = APIRouter()


class CourseData(BaseModel):
    course_code: str
    course_name: str
    credits: int


class CourseUpdate(BaseModel):
    course_name: str


@router.get("/courses")
def get_courses():
    courses = service_get_courses()

    return [
        {
            "course_code": c.course_code,
            "course_name": c.course_name,
            "credits": c.credits
        }
        for c in courses
    ]


@router.post("/courses")
def create_course(data: CourseData):
    course = Course(
        course_code=data.course_code,
        course_name=data.course_name,
        credits=data.credits
    )

    course_code = data.course_code

    service_add_course(course)

    return {
        "message": "Course added successfully",
        "course_code": course_code
    }


@router.get("/courses/{course_code}")
def get_course(course_code: str):
    courses = service_get_courses()

    for c in courses:
        if c.course_code == course_code:
            return {
                "course_code": c.course_code,
                "course_name": c.course_name,
                "credits": c.credits
            }

    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )


@router.put("/courses/{course_code}")
def update_course(course_code: str, data: CourseUpdate):
    success = service_update_course(course_code, data.course_name)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return {
        "message": "Course updated successfully",
        "course_code": course_code
    }


@router.delete("/courses/{course_code}")
def delete_course(course_code: str):
    success = service_delete_course(course_code)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return {
        "message": "Course deleted successfully",
        "course_code": course_code
    }
