
import constants
from dao.db_connection import get_db
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import traceback

from model.api.SignMessageRequest import SignMessageRequest
from model.api.VerifySignatureRequest import VerifySignatureRequest
from model.dao.SenderMessage import SenderMessage
from model.internal.User import User

import utils.user_util
import utils.rsa_util

import dao.sender_messages_dao

app = FastAPI()

# Add CORS middleware, This is required while running FastAPI locally.
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
        sender_id = utils.user_util.get_id_from_email(request.user)
        private_key = constants.private_keys[sender_id]

        encoded_signature = utils.rsa_util.get_encoded_signature(private_key, request.message)
        print(f"Generated Signature: {encoded_signature}...")

        # Change private key id when multiple private key ids are supported. Currently using sender_id as private key id
        sender_message = SenderMessage(sender_id=sender_id, private_key_id=sender_id,
            message=request.message, signature=encoded_signature)
        dao.sender_messages_dao.add_sender_message(sender_message, db)
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
        sender_id = utils.user_util.get_id_from_email(request.user)
        public_key = constants.private_keys[sender_id].public_key()

        is_valid = utils.rsa_util.verify_signature(public_key, request.message, request.signature)
        print(f"Signature verification status is {is_valid}...")
        return {"valid": is_valid}
    except Exception as e:
        print(f"Exception occurred while verifying signature!: message: {str(e)}")
        traceback.print_exc()
        return {"valid": False}

# Run using: uvicorn filename:app --reload

