
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.database import models
from app.database.db import engine

from app.api import student
from app.api import faculty
from app.api import courses
from app.api import enrollments
from app.api import auth
from app.api import reports

from app.core.logger import logger


# Load environment settings
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# Create database tables without deleting existing records
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CampusHub ERP")


# Login session support
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv(
        "SESSION_SECRET",
        "temporary-development-secret-change-this"
    ),
    max_age=3600,
    same_site="lax",
    https_only=False
)


logger.info("CampusHub ERP application started")


# Check whether user is logged in
def require_login(request: Request):
    if not request.session.get("user_id"):
        raise HTTPException(
            status_code=401,
            detail="Please login first."
        )


# Serve CSS and JavaScript files
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


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


# Protected API routes
app.include_router(
    student.router,
    dependencies=[Depends(require_login)]
)

app.include_router(
    faculty.router,
    dependencies=[Depends(require_login)]
)

app.include_router(
    courses.router,
    dependencies=[Depends(require_login)]
)

app.include_router(
    enrollments.router,
    dependencies=[Depends(require_login)]
)

app.include_router(
    reports.router,
    dependencies=[Depends(require_login)]
)


# Public authentication routes
app.include_router(auth.router)


# Public website homepage
@app.get("/")
def home():
    logger.info("CampusHub ERP website opened")

    return FileResponse(
        BASE_DIR / "templates" / "index.html"
    )
