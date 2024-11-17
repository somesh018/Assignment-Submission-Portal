import bcrypt

def hash_password(password):
    """Hash a password."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(input_password, stored_password):
    """Verify if the input password matches the stored hashed password."""
    if isinstance(input_password, str):
        input_password = input_password.encode('utf-8')
    if isinstance(stored_password, str):
        stored_password = stored_password.encode('utf-8')
    
    return bcrypt.checkpw(input_password, stored_password)
