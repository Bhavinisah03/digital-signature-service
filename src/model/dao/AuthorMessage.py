from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import PrimaryKeyConstraint
from dao.db_connection import Base

# ✅ Define Existing Table Structure (must match your existing table)
class AuthorMessage(Base):
    __tablename__ = "author_messages"  # Ensure this matches your table name
    author_id = Column(Integer, nullable=False)
    private_key_id = Column(Integer, nullable=False)
    message = Column(String, nullable=False)
    signature = Column(String, nullable=False)

    # ✅ Define Composite Primary Key
    __table_args__ = (PrimaryKeyConstraint("author_id", "private_key_id", "message", "signature"),)