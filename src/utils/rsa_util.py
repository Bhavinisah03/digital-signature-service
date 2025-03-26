from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import constants
import base64
import traceback

def get_private_keys():
    private_keys = {}
    for user in constants.users:
        id = user.id
        private_keys[id] = rsa.generate_private_key(public_exponent=constants.public_exponent_num,
            key_size=constants.rsa_key_size)
    return private_keys

def sign_message(private_key: str, message: str):
    signature = private_key.sign(
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    return signature

def get_encoded_signature(private_key: str, message: str):
    signature = sign_message(private_key, message)
    encoded_signature = base64.b64encode(signature).decode()

    return encoded_signature

#### Returns True if signature was created for message, False otherwise.
def verify_signature(public_key: str, message: str, signature: str):
    is_valid = False
    try:
        decoded_signature = base64.b64decode(signature)
        public_key.verify(
                decoded_signature, message.encode(),
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
             )
        is_valid = True
    except Exception as e:
        print(f"Exception occurred while verifying signature, this means signature is invalid!: message: {str(e)}")
        traceback.print_exc()
        is_valid = False
    return is_valid
