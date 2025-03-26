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