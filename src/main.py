
import constants
from dao.db_connection import get_db
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import traceback

from model.api.SignMessageRequest import SignMessageRequest
from model.api.VerifySignatureRequest import VerifySignatureRequest
from model.api.VerifyAuthorCredentialRequest import VerifyAuthorCredentialRequest
from model.api.AddOrUpdateUserCredentialRequest import AddOrUpdateUserCredentialRequest
from model.dao.AuthorMessage import AuthorMessage
from model.dao.UserCredentials import UserCredentials
# {
#   "email": "bhavini.1@gmail.com",
#   "password": "test1234",
#   "user_type": "Admina"
# }
from model.internal.User import User

import utils.user_util
import utils.rsa_util

import dao.user_credentials_dao
import dao.author_messages_dao

app = FastAPI()

# Add CORS middleware, This is required while running FastAPI locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL for security (e.g., ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Endpoint to sign a message
@app.post("/sign/")
def sign_message(request: SignMessageRequest, db: Session = Depends(get_db)):
    print(f"Signing message. signMessageRequest: {request}...")
    try:
        author_id = utils.user_util.get_id_from_email(request.user)
        private_key = constants.private_keys[author_id]

        encoded_signature = utils.rsa_util.get_encoded_signature(private_key, request.message)
        print(f"Generated Signature: {encoded_signature}...")

        # Change private key id when multiple private key ids are supported. Currently using author_id as private key id
        author_message = AuthorMessage(author_id=author_id, private_key_id=author_id,
            message=request.message, signature=encoded_signature)
        dao.author_messages_dao.add_author_message(author_message, db)
        return {"message": request.message, "signature": encoded_signature, "user": request.user}
    except Exception as e:
        print(f"exception occurred: message: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to verify a signature
@app.post("/verify/")
def verify_signature(request: VerifySignatureRequest):
    try:
        print(f"Verifying signature. verifySignatureRequest: {request}...")
        author_id = utils.user_util.get_id_from_email(request.user)
        public_key = constants.private_keys[author_id].public_key()

        is_valid = utils.rsa_util.verify_signature(public_key, request.message, request.signature)
        print(f"Signature verification status is {is_valid}...")
        return {"valid": is_valid}
    except Exception as e:
        print(f"Exception occurred while verifying signature!: message: {str(e)}")
        traceback.print_exc()
        return {"valid": False}


# Endpoint to verify a signature
@app.post("/verify_author_credential/")
def verify_signature(request: VerifyAuthorCredentialRequest):
    try:
        print(f"Verifying author's credentials. verifyAuthorCredentialRequest: {request}...")
        author_id = utils.user_util.get_id_from_email(request.user)
        public_key = constants.private_keys[author_id].public_key()

        is_valid = utils.rsa_util.verify_signature(public_key, request.message, request.signature)
        print(f"Signature verification status is {is_valid}...")
        return {"valid": is_valid}
    except Exception as e:
        print(f"Exception occurred while verifying signature!: message: {str(e)}")
        traceback.print_exc()
        return {"valid": False}


# ✅ API to Insert Data into Existing SQLite Table
@app.post("/add_or_update_user_credentials/")
def add_or_update_user_credentials(request: AddOrUpdateUserCredentialRequest, db: Session = Depends(get_db)):
    print(f"Adding user credentials for user: {request.email} and user_type: {request.user_type}...")
    try:
        if request.user_type not in constants.SUPPORTED_USER_TYPES:
            return {"status": "Failure", "message": f"User type: {request.user_type} is not support"}

#         encrypted_password = utils.password_util.encrypt_password(request.password)
#         user_credentials = UserCredentials(email=request.email, password=encrypted_password, user_type=request.user_type)
#
#         print(f"Adding user credentials: {user_credentials}...")
#
#         db.merge(user_credentials)
#         db.commit()

        dao.user_credentials_dao.add_or_update_user_credentials(request.email, request.password, request.user_type, db)

#         print(f"User credentials is added successfully for user: {request.email} and user_type: {request.user_type}...")

        return {"status": "Success"}
    except Exception as e:
        print(f"exception occurred file adding User credentials for user: {request.email} and user_type: {request.user_type}! message: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Run using: uvicorn filename:app --reload

