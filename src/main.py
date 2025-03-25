from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from fastapi.middleware.cors import CORSMiddleware
import base64

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL for security (e.g., ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

users = ["bhavini.1@gmail.com", "bhavini.2@gmail.com"]
private_keys = {}

# Generate RSA key pair
public_exponent_num = 65537
for user in users:
    private_keys[user] = rsa.generate_private_key(public_exponent=public_exponent_num, key_size=2048)
#
# private_key =
# print(f"private_key: {private_key}")
#
# private_key1 = rsa.generate_private_key(public_exponent=public_exponent_num, key_size=2048)
# print(f"private_key1: {private_key1}")

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
def sign_message(request: MessageRequest):
    try:
        user = request.user
        private_key = private_keys[user]
        signature = private_key.sign(
            request.message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        encoded_signature = base64.b64encode(signature).decode()
        return {"message": request.message, "signature": encoded_signature, "user": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to verify a signature
@app.post("/verify/")
def verify_signature(request: VerifyRequest):
    try:
        decoded_signature = base64.b64decode(request.signature)
        public_key = private_keys[request.user].public_key()
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

# Run using: uvicorn filename:app --reload


