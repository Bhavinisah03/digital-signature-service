class User():
    def __init__(self, email, id):  # Constructor
            self.email = email
            self.id = id
    def __str__(self):
        return f"User(email={self.email}, id={self.id})"

