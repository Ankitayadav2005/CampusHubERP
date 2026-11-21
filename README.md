
# CampusHub ERP

CampusHub ERP is a Python-based Student Management System built using FastAPI and SQLite.

## Features

- Student CRUD operations
- Faculty CRUD operations
- Course CRUD operations
- Enrollment CRUD operations
- Email validation
- SQLite database integration
- Repository Pattern
- Service Layer
- Singleton Pattern
- Factory Pattern
- Application logging
- JSON data export
- Text report generation
- Automated testing using Pytest

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pytest
- HTTPX

## Installation

Install dependencies:

    python -m pip install -r requirements.txt

## Run Application

    python -m uvicorn app.main:app --reload

## API Documentation

http://127.0.0.1:8000/docs

## Run Tests

    python -m pytest -v

## Export Data and Generate Reports

    python -m app.utils.data_manager

## Database

The project uses SQLite database: campushub.db.
