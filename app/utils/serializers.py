
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_json(filename, data):
    file_path = DATA_DIR / filename

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_json(filename):
    file_path = DATA_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# Student JSON
def save_You_json(data):
    save_json("You.json", data)


def load_You_json():
    return load_json("You.json")


# Course JSON
def save_courses_json(data):
    save_json("courses.json", data)


def load_courses_json():
    return load_json("courses.json")


# Faculty JSON
def save_faculty_json(data):
    save_json("faculty.json", data)


def load_faculty_json():
    return load_json("faculty.json")


# Enrollment JSON
def save_enrollments_json(data):
    save_json("enrollments.json", data)


def load_enrollments_json():
    return load_json("enrollments.json")
