
# CampusHub ERP

CampusHub ERP is a Python-based Student Management System built using FastAPI and SQLite.

## Features

- Student CRUD operations
- Faculty CRUD operations
- Course CRUD operations
- Enrollment CRUD operations
- Email validation
- Database integration using SQLite
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

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python -m uvicorn app.main:app --reload
```

## API Documentation

Open this URL in your browser:

http://127.0.0.1:8000/docs

## Run Tests

```bash
python -m pytest -v
```

## Export Data and Generate Reports

```bash
python -m app.utils.data_manager
```

## Project Structure

- app/ - Main application source code
- app/api/ - API routes
- app/core/ - Core utilities and design patterns
- app/database/ - Database and repository
- app/models/ - Data models
- app/services/ - Service layer
- app/utils/ - Utility functions
- data/ - JSON exported data
- reports/ - Generated text reports
- logs/ - Application logs
- tests/ - Automated tests

## Database

The project uses SQLite database: `campushub.db`.
