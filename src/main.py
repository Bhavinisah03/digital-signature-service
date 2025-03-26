
import constants
from dao.db_connection import get_db
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Security
from sqlalchemy.orm import Session
import traceback

from model.api.AddOrUpdateUserCredentialRequest import AddOrUpdateUserCredentialRequest
from model.api.SignMessageRequest import SignMessageRequest
from model.api.VerifyAuthorRequest import VerifyAuthorRequest
from model.api.VerifyAuthorCredentialRequest import VerifyAuthorCredentialRequest
from model.api.VerifySignatureRequest import VerifySignatureRequest

from model.dao.AuthorMessage import AuthorMessage
from model.dao.UserCredentials import UserCredentials

from model.internal.User import User

import utils.user_util
import utils.rsa_util
import utils.access_token_util

import dao.user_credentials_dao
import dao.author_messages_dao

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Add CORS middleware, This is required while running FastAPI locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL for security (e.g., ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

def get_current_user(access_token: str = Security(oauth2_scheme)):
    print(f"Check if current user is authenticated...")
    payload = utils.access_token_util.verify_token(access_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Unauthorized User. Invalid token.")
    return payload

# Endpoint to sign a message
@app.post("/sign/")
def sign_message(request: SignMessageRequest, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    email = user['sub']
    print(f"Signing message for user: {email}. signMessageRequest: {request}...")
    try:
        author_id = utils.user_util.get_id_from_email(email)
        private_key = constants.private_keys[author_id]

        encoded_signature = utils.rsa_util.get_encoded_signature(private_key, request.message)
        print(f"Generated Signature: {encoded_signature}...")

        # Change private key id when multiple private key ids are supported. Currently using author_id as private key id
        author_message = AuthorMessage(author_id=author_id, private_key_id=author_id,
            message=request.message, signature=encoded_signature)
        dao.author_messages_dao.add_author_message(author_message, db)
        return {"message": request.message, "signature": encoded_signature, "user": email}
    except HTTPException as e:
        traceback.print_exc()
        raise e
    except Exception as e:
        print(f"exception occurred: message: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal error while signing the message. Please try again")

@app.get("/verify_token")
def verify_token_endpoint(user: dict = Depends(get_current_user)):
    print(f"verify_token_endpoint. user: {user}...")
    return {"message": "Token is valid"}

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
def verify_author_credential(request: VerifyAuthorCredentialRequest, db: Session = Depends(get_db)):
    try:
        is_valid_author = dao.user_credentials_dao.user_exists(request.email, request.password, "Author", db)
        return {"valid": is_valid_author}
    except Exception as e:
        print(f"Exception occurred while verifying signature!: message: {str(e)}")
        traceback.print_exc()
        return {"valid": False}

@app.post("/author_login")
def author_login(request: VerifyAuthorRequest, db: Session = Depends(get_db)):
    try:
        print(f"Trying to login author with email: {request.username}...")
        is_valid_author = dao.user_credentials_dao.user_exists(request.username, request.password, "Author", db)

        if is_valid_author:
            access_token = utils.access_token_util.create_access_token({"sub": request.username})
            response = {"valid": is_valid_author, "access_token": access_token, "token_type": "bearer"}
        else:
            response = {"valid": False}
        print(f"Returning login response: {response}...")
        return response
    except Exception as e:
        print(f"Exception occurred while verifying signature!: message: {str(e)}")
        traceback.print_exc()
        return {"valid": False}

# ✅ API to Insert Data into user_credentials table
@app.post("/add_or_update_user_credentials/")
def add_or_update_user_credentials(request: AddOrUpdateUserCredentialRequest, db: Session = Depends(get_db)):
    print(f"Adding user credentials for user: {request.email} and user_type: {request.user_type}...")
    try:
        if request.user_type not in constants.SUPPORTED_USER_TYPES:
            return {"status": "Failure", "message": f"User type: {request.user_type} is not support"}

        dao.user_credentials_dao.add_or_update_user_credentials(request.email, request.password, request.user_type, db)
        return {"status": "Success"}
    except Exception as e:
        print(f"exception occurred file adding User credentials for user: {request.email} and user_type: {request.user_type}! message: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Run using: uvicorn filename:app --reload

