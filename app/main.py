from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.database import models
from app.database.db import engine

from app.api import student
from app.api import faculty
from app.api import courses
from app.api import enrollments

from app.core.logger import logger


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CampusHub ERP")

logger.info("CampusHub ERP application started")


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.error(
        f"Unexpected error at {request.url.path}: {exc}",
        exc_info=True
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error. Please try again later."
        }
    )


app.include_router(student.router)
app.include_router(faculty.router)
app.include_router(courses.router)
app.include_router(enrollments.router)


@app.get("/")
def home():
    logger.info("Home endpoint accessed")
    return {"message": "CampusHub ERP API is running"}
