
from pydantic import BaseModel

# ✅ Pydantic Model for Request Body
class CreateAuthorMessageRequest(BaseModel):
    author_id: int
    private_key_id: int
    message: str
    signature: str