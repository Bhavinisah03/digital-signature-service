from datetime import datetime, timedelta
from jose import JWTError, jwt

ALGORITHM = "HS256"
ACCESS_SECRET_KEY = "Huhdfuhsd78686JJSHD97979"
ACCESS_TOKEN_EXPIRE_IN_MINUTES = 30  # Session expires after 30 mins

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_IN_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, ACCESS_SECRET_KEY, algorithm=ALGORITHM)

# Returns None is access token is expired, non None otherwise
def verify_token(access_token: str):
    try:
        access_payload = jwt.decode(access_token, ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
        return access_payload  # Returns decoded user data if valid
    except JWTError:
        return None  # Invalid or expired token
