
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database.models import Faculty
from app.services.repository_faculty_service import (
    add_faculty as service_add_faculty,
    get_faculty as service_get_faculty,
    update_faculty as service_update_faculty,
    delete_faculty as service_delete_faculty
)

router = APIRouter()


class FacultyData(BaseModel):
    faculty_id: str
    name: str
    age: int
    email: str
    department: str


class FacultyUpdate(BaseModel):
    name: str


@router.get("/faculty")
def get_faculty():
    faculty_list = service_get_faculty()

    return [
        {
            "faculty_id": f.faculty_id,
            "name": f.name,
            "age": f.age,
            "email": f.email,
            "department": f.department
        }
        for f in faculty_list
    ]


@router.post("/faculty")
def create_faculty(data: FacultyData):
    faculty = Faculty(
        faculty_id=data.faculty_id,
        name=data.name,
        age=data.age,
        email=data.email,
        department=data.department
    )

    faculty_id = data.faculty_id

    service_add_faculty(faculty)

    return {
        "message": "Faculty added successfully",
        "faculty_id": faculty_id
    }


@router.get("/faculty/{faculty_id}")
def get_faculty_by_id(faculty_id: str):
    faculty_list = service_get_faculty()

    for f in faculty_list:
        if f.faculty_id == faculty_id:
            return {
                "faculty_id": f.faculty_id,
                "name": f.name,
                "age": f.age,
                "email": f.email,
                "department": f.department
            }

    raise HTTPException(
        status_code=404,
        detail="Faculty not found"
    )


@router.put("/faculty/{faculty_id}")
def update_faculty(faculty_id: str, data: FacultyUpdate):
    success = service_update_faculty(faculty_id, data.name)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Faculty not found"
        )

    return {
        "message": "Faculty updated successfully",
        "faculty_id": faculty_id
    }


@router.delete("/faculty/{faculty_id}")
def delete_faculty(faculty_id: str):
    success = service_delete_faculty(faculty_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Faculty not found"
        )

    return {
        "message": "Faculty deleted successfully",
        "faculty_id": faculty_id
    }
