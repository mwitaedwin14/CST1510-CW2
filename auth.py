import hashlib
import bcrypt
import os

def hash_password(plain_text_password):

    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt(rounds = 12)

    hash_password = bcrypt.hashpw(password_bytes, salt)
    return hash_password

user_input = input('Enter your password:')
hash_text_password = hash_password(user_input)
print(f"Hashed password: {hash_text_password}")

def verify_password(plain_text_password, hash_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hash_text_password)

test_password = "SecurePassword123"
#Test hashing
hashed = hash_password(test_password)
print(f"Original Password: {test_password}")
print(f"Hashed Password: {hashed}")
print(f"Hash length: {len(hashed)} characters")

#Test verification with correct password
is_valid = verify_password(test_password, hashed)
print(f"\nVerification result: {is_valid}")

#Test verification with wrong password
is_valid_wrong = verify_password("WrongPassword", hashed)
print(f"\nVerification result: {is_valid_wrong}")

USER_DATA_FILE = "users.txt"

def register_user(username, password):
    hash_text_password = hash_password(password)
    with open("users.txt", 'a') as file:



