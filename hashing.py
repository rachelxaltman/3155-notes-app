import hashlib

class Encryption():

    def __init__(self):
        self.hasher = hashlib.sha256()

    def encrypt(self, password):
        self.hasher.update(password.encode())
        return self.hasher.digest()

    def check_encrypted_password(self, password, hashed):
        if password == hashed:
            return True
        return False
