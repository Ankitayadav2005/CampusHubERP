# CampusHub ERP

CampusHub ERP is a web-based College Management System developed using Python, FastAPI, SQLAlchemy, and SQLite. It provides a centralized platform to manage students, faculty, courses, and enrollments.

## Features

### 1. Dashboard
- Web-based management dashboard
- Overview of students, faculty, courses, and enrollments

### 2. Student Management
- Add, view, update, and delete student records
- Student information management
- Email validation

### 3. Faculty Management
- Add, view, update, and delete faculty records
- Faculty information management

### 4. Course Management
- Add, view, update, and delete courses
- Course information and credit management

### 5. Enrollment Management
- Manage student course enrollments
- Update and delete enrollment records
- Validate student and course references

### 6. Authentication
- User registration and login
- Session-based authentication
- Forgot password and password reset functionality

### 7. Reports
- Download student, faculty, course, and enrollment reports in PDF format
- Export reports to Excel

### 8. Additional Features
- SQLite database integration
- Repository Pattern
- Service Layer
- Singleton Pattern
- Factory Pattern
- Application logging
- JSON data export
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

## Project Installation

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Open Project Folder

```bash
cd CampusHubERP
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Run Application

```bash
python -m uvicorn app.main:app --reload
```

## Application URLs

- Website: http://127.0.0.1:8000
- API Documentation: http://127.0.0.1:8000/docs

## Run Automated Tests

```bash
python -m pytest -v
```

The project currently has 14 passing automated tests.

## Database

The application uses SQLite for storing user, student, faculty, course, and enrollment information.

Database file: `campushub.db`

## Project Structure

```text
CampusHubERP/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── services/
│   ├── static/
│   ├── templates/
│   ├── utils/
│   └── main.py
│
├── tests/
├── reports/
├── data/
├── requirements.txt
├── README.md
├── pytest.ini
└── campushub.db
```

## Project Purpose

The purpose of CampusHub ERP is to simplify college administration by providing a centralized system for managing student records, faculty details, courses, enrollments, and reports.

## Testing

All 14 automated tests are currently passing.

---

**CampusHub ERP – College Management Made Easier.**
