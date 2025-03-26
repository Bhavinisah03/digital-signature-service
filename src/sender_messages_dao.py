from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


# ✅ Replace this with your existing database file
DATABASE_URL = "sqlite:///../db/digital_signatures.db"

# ✅ Set up database connection
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Define SQLAlchemy Base
Base = declarative_base()

# ✅ Define Existing Table Structure (must match your existing table)
class SenderMessage(Base):
    __tablename__ = "sender_messages"  # Ensure this matches your table name
    sender_id = Column(Integer, nullable=False)
    private_key_id = Column(Integer, nullable=False)
    message = Column(String, nullable=False)
    signature = Column(String, nullable=False)

    # ✅ Define Composite Primary Key
    __table_args__ = (PrimaryKeyConstraint("sender_id", "private_key_id", "message", "signature"),)

# ✅ Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Pydantic Model for Request Body
class CreateSenderMessageRequest(BaseModel):
    sender_id: int
    private_key_id: int
    message: str
    signature: str