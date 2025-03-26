
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from sqlalchemy import create_engine

# Define Base class (SQLAlchemy 2.0 style)
class Base(DeclarativeBase):
    pass

# ✅ Replace this with your existing database file
DATABASE_URL = "sqlite:///../db/digital_signatures.db"
# ✅ Set up database connection
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


