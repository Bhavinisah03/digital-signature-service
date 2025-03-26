from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import PrimaryKeyConstraint
from dao.db_connection import Base

# ✅ Define Existing Table Structure (must match your existing table)
class UserCredentials(Base):
    __tablename__ = "user_credentials"  # Ensure this matches your table name
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    user_type = Column(String, nullable=False)

    # ✅ Define Composite Primary Key
    __table_args__ = (PrimaryKeyConstraint("email", "user_type"),)

    def __str__(self):
        return f"UserCredentials(email={self.email}, password={self.password}, user_type: {self.user_type})"