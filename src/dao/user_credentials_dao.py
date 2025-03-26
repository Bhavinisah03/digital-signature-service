from sqlalchemy.orm import Session
from model.dao.UserCredentials import UserCredentials
import utils.password_util

# ✅ API to Insert Data into Existing SQLite Table
def add_or_update_user_credentials(email: str, password: str, user_type: str, db: Session):
    encrypted_password = utils.password_util.encrypt_password(password)
    user_credentials = UserCredentials(email=email, password=encrypted_password, user_type=user_type)

    print(f"Adding user credentials: {user_credentials}...")
    db.merge(user_credentials)
    db.commit()
    print(f"User credentials is added successfully for user: {email} and user_type: {user_type}...")

def user_exists(email: str, password: str, user_type: str, db: Session) -> bool:
    print(f"Checking if user exists for email: {email}, password: {password}, user_type: {user_type}...")

    user_credentials = db.query(UserCredentials).filter(UserCredentials.email == email, UserCredentials.user_type == user_type).first()
    does_user_exists = False
    if user_credentials is not None:
        print(f"First record for email: {email}, password: {password}, user_type: {user_type} is user_credentials: {user_credentials}.")
        does_user_exists = utils.password_util.verify_password(password, user_credentials.password)

    print(f"Status for checking user exists for email: {email}, password: {password}, user_type: {user_type} is does_user_exists: {does_user_exists}...")
    return does_user_exists