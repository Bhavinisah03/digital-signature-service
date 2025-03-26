from pydantic import BaseModel

class AddOrUpdateUserCredentialRequest(BaseModel):
    email: str
    password: str
    user_type: str

