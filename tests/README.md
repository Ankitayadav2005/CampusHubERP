# CampusHub ERP

CampusHub ERP is a web-based College Management System developed using Python, FastAPI, SQLAlchemy, and SQLite.

## Features

- Web-based management dashboard
- Student CRUD operations
- Faculty CRUD operations
- Course CRUD operations
- Enrollment CRUD operations
- User registration and login
- Session-based authentication
- Forgot password and password reset
- Email validation
- SQLite database integration
- Repository Pattern and Service Layer
- Singleton Pattern and Factory Pattern
- Application logging
- JSON data export
- PDF report downloads
- Excel report downloads
- Automated testing using Pytest

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- HTML
- CSS
- JavaScript
- Pytest
- HTTPX
- ReportLab
- OpenPyXL

## Installation

Install dependencies:

    python -m pip install -r requirements.txt

## Run Application

    python -m uvicorn app.main:app --reload

## Application URLs

Website: http://127.0.0.1:8000

API Documentation: http://127.0.0.1:8000/docs

## Run Tests

    python -m pytest -v

Current test result: 14 tests passed.

## Reports

The application supports PDF and Excel report downloads for:

- Students
- Faculty
- Courses
- Enrollments

## Database

The application uses SQLite database: campushub.db

## Project Purpose

CampusHub ERP aims to simplify college administration by providing a centralized platform for managing student records, faculty details, courses, enrollments, and reports.

---

CampusHub ERP - College Management Made Easier.