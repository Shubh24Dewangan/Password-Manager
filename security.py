import hashlib
from cryptography.fernet import Fernet
from config import secretKey

fernet = Fernet(secretKey)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def encrypt_password(password):
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(password):
    return fernet.decrypt(password.encode()).decode()

