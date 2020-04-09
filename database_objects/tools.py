import hashlib



def encode(password: str):
    # Encode user password
    m = hashlib.sha256()
    m.update(bytes(password, 'utf8'))
    return m.hexdigest()