import hashlib

def hashed_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
