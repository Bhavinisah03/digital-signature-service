from pydantic import BaseModel

class VerifyAuthorCredentialRequest(BaseModel):
    email: str
    password: str

