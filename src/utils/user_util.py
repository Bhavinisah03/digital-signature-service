import constants

def get_id_from_email(email: str):
    print(f"Searching for matching_user with email: {email} in users: {constants.users}...")
    matching_user = next((user for user in constants.users if email == user.email),None)
    if matching_user is None:
        msg = f"matching user not found for email:{email}!"
        print(msg)
        raise KeyError(msg)
    print(f"matching user found for email:{matching_user.email} with id:{matching_user.id}!")
    return matching_user.id


