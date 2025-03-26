from pydantic import BaseModel

class SignMessageRequest(BaseModel):
    message: str

