import bcrypt

def encrypt_password(password: str) -> str:
    print(f"Encrypting password...")
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    encrypted_password = hashed_password.decode()  # Convert to string for storage
    print("Encrypted password:", encrypt_password)
    return encrypted_password

def verify_password(password: str, hashed_password: str) -> bool:
    print(f"Verifying password...")
    is_valid = bcrypt.checkpw(password.encode(), hashed_password.encode())
    print(f"Password verification status: {is_valid}.")
    return is_valid


