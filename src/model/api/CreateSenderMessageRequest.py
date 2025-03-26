
from pydantic import BaseModel

# ✅ Pydantic Model for Request Body
class CreateSenderMessageRequest(BaseModel):
    sender_id: int
    private_key_id: int
    message: str
    signature: str