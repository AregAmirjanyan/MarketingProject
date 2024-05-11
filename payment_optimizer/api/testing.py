import bcrypt

def hash_password(password: str) -> str:
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    # Verify the password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Example usage
password = "my_secure_password"
hashed_password = hash_password(password)

# Example of verifying password
is_valid = verify_password(password, hashed_password)
print("Password is valid:", is_valid)