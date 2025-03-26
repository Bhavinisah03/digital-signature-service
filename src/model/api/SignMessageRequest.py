from pydantic import BaseModel

class SignMessageRequest(BaseModel):
    message: str
    user: str

