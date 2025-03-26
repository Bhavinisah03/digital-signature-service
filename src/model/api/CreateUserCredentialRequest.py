
from pydantic import BaseModel

# ✅ Pydantic Model for Request Body
class CreateUserCredentialRequest(BaseModel):
    email: str
    password: str
    user_type: str