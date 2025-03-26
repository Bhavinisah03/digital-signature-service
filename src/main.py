from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from fastapi.middleware.cors import CORSMiddleware
import base64
import traceback

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.schema import PrimaryKeyConstraint


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL for security (e.g., ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
class User():
    def __init__(self, email, id):  # Constructor
            self.email = email  # Instance variable
            self.id = id    # Instance variable
    def __str__(self):
        return f"User(email={self.email}, id={self.id})"

users = [User(email="bhavini.1@gmail.com", id=1), User(email="bhavini.2@gmail.com", id=2)]
private_keys = {}

# Generate RSA key pair
public_exponent_num = 65537
for user in users:
    id = user.id
    private_keys[id] = rsa.generate_private_key(public_exponent=public_exponent_num, key_size=2048)
#
# private_key =
# print(f"private_key: {private_key}")
#
# private_key1 = rsa.generate_private_key(public_exponent=public_exponent_num, key_size=2048)
# print(f"private_key1: {private_key1}")

###################
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


# ✅ Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Define SQLAlchemy Base
Base = declarative_base()
# db = get_db()

# ✅ Define Existing Table Structure (must match your existing table)
class SenderMessage(Base):
    __tablename__ = "sender_messages"  # Ensure this matches your table name
    sender_id = Column(Integer, nullable=False)
    private_key_id = Column(Integer, nullable=False)
    message = Column(String, nullable=False)
    signature = Column(String, nullable=False)

    # ✅ Define Composite Primary Key
    __table_args__ = (PrimaryKeyConstraint("sender_id", "private_key_id", "message", "signature"),)


# ✅ Pydantic Model for Request Body
class CreateSenderMessageRequest(BaseModel):
    sender_id: int
    private_key_id: int
    message: str
    signature: str
###################
# Request models
class MessageRequest(BaseModel):
    message: str
    user: str

class VerifyRequest(BaseModel):
    message: str
    signature: str
    user: str

# Endpoint to sign a message
@app.post("/sign/")
def sign_message(request: MessageRequest, db: Session = Depends(get_db)):
    print(f"Signing message. messageRequest: {request}...")
    try:
        sender_id = get_id_from_email(request.user)
        private_key = private_keys[sender_id]
        signature = private_key.sign(
            request.message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        encoded_signature = base64.b64encode(signature).decode()
        print(f"Generated Signature: {encoded_signature}...")
        # Change private key id when multiple private key ids are supported. Currently using sender_id as private key id
        sender_message = SenderMessage(sender_id=sender_id, private_key_id=sender_id,
            message=request.message, signature=encoded_signature)
        add_sender_message(sender_message, db)
        return {"message": request.message, "signature": encoded_signature, "user": user}
    except Exception as e:
        print(f"exception occurred: message: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to verify a signature
@app.post("/verify/")
def verify_signature(request: VerifyRequest):
    try:
        sender_id = get_id_from_email(request.user)
        decoded_signature = base64.b64decode(request.signature)
        public_key = private_keys[sender_id].public_key()
        public_key.verify(
            decoded_signature,
            request.message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return {"valid": True}
    except Exception:
        return {"valid": False}

def get_id_from_email(email: str):
    print(f"Searching for matching_user with email: {email} in users: {users}...")
    matching_user = next((user for user in users if email == user.email),None)
    if matching_user is None:
        msg = f"matching user not found for email:{email}!"
        print(msg)
        raise KeyError(msg)
    print(f"matching user found for email:{matching_user.email} with id:{matching_user.id}!")
    return matching_user.id

# ✅ API to Insert Data into Existing SQLite Table
def add_sender_message(sender_message: SenderMessage, db: Session):
    print(f"Adding sender message to DB. sender_message: {sender_message}...")
    db.add(sender_message)
    db.commit()
    db.refresh(sender_message)
    print(f"Sender message added to DB. sender_message: {sender_message}...")
# Run using: uvicorn filename:app --reload

#
# # ✅ API to Insert Data into Existing SQLite Table
# @app.post("/add_user/")
# def add_sender_message(request: CreateSenderMessageRequest, db: Session = Depends(get_db)):
#
#     sender_message = SenderMessage(sender_id=request.sender_id, private_key_id=request.private_key_id,
#     message=request.message, signature=request.signature)
#
#     db.add(sender_message)
#     db.commit()
#     db.refresh(sender_message)
#     return {"message": "Sender message added successfully", "sender_message": sender_message}
# # Run using: uvicorn filename:app --reload


