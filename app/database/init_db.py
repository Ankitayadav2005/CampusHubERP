from app.database.db import engine, Base
from app.database.models import Student, Faculty, Course


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    create_tables()