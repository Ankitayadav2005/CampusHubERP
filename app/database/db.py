
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///campushub.db"


class DatabaseSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.engine = create_engine(DATABASE_URL)

            cls._instance.SessionLocal = sessionmaker(
                bind=cls._instance.engine,
                autoflush=False,
                autocommit=False
            )

        return cls._instance


# Singleton database manager
database = DatabaseSingleton()

# Existing project compatibility
engine = database.engine
SessionLocal = database.SessionLocal

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
