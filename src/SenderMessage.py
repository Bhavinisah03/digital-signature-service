from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# ✅ Define Existing Table Structure (must match your existing table)
class SenderMessage(Base):
    __tablename__ = "sender_messages"  # Ensure this matches your table name
    sender_id = Column(Integer, nullable=False)
    private_key_id = Column(Integer, nullable=False)
    message = Column(String, nullable=False)
    signature = Column(String, nullable=False)

    # ✅ Define Composite Primary Key
    __table_args__ = (PrimaryKeyConstraint("sender_id", "private_key_id", "message", "signature"),)