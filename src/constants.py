from model.internal.User import User
from utils.rsa_util import get_private_keys

users = [User(email="bhavini.1@gmail.com", id=1), User(email="bhavini.2@gmail.com", id=2)]

# Generate RSA key pair
public_exponent_num = 65537

rsa_key_size = 2048

private_keys = get_private_keys()