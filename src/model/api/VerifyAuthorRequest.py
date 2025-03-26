from pydantic import BaseModel

class VerifyAuthorRequest(BaseModel):
    username: str
    password: str

