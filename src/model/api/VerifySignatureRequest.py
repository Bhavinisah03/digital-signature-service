from pydantic import BaseModel

class VerifySignatureRequest(BaseModel):
    message: str
    signature: str
    user: str

