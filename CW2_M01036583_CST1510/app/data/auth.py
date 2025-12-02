import bcrypt
import os
import re

# Constant for user data storage
USER_DATA_FILE = "users.txt"


def hash_password(plain_text_password: str) -> str:
    """Hashes a password using bcrypt with automatic salt generation."""
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')  # Store as string in file


def verify_password(plain_text_password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against a stored bcrypt hash."""
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def user_exists(username: str) -> bool:
    """Check if a username already exists in users.txt."""
    if not os.path.exists(USER_DATA_FILE):
        return False
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            if line.strip():
                stored_username = line.split(",")[0]
                if stored_username == username:
                    return True
    return False


def register_user(username: str, password: str) -> bool:
    """Register a new user if username doesn't exist."""
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False

    hashed = hash_password(password)
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{hashed}\n")

    print(f"Success: User '{username}' registered successfully!")
    return True

def login_user(username: str, password: str) -> bool:
    """Authenticate user by username and password."""
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False

    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            if line.strip():
                stored_username, stored_hash = line.strip().split(",", 1)
                if stored_username == username:
                    if verify_password(password, stored_hash):
                        print(f"Success: Welcome, {username}!")
                        return True
                    else:
                        print("Error: Invalid password.")
                        return False
        print("Error: Username not found.")
        return False


def validate_username(username: str):
    """Validate username: 3-20 chars, alphanumeric + underscore only."""
    if not (3 <= len(username) <= 20):
        return False, "Username must be 3-20 characters long."
    if not re.match("^[a-zA-Z0-9_]+$", username):
        return False, "Username can only contain letters, numbers, and underscores."
    return True, ""


def validate_password(password: str):
    """Validate password: min 8 chars, with uppercase, lowercase, digit, special char."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, ""


def check_password_strength(password: str) -> str:
    """Return Weak, Medium, or Strong based on password criteria."""
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    if re.search(r"[a-z]", password) and re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    if len(password) >= 12:
        score += 1

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"


# ======================
# Interactive Interface
# ======================

def display_menu():
    print("\n" + "=" * 50)
    print("  MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("  Secure Authentication System")
    print("=" * 50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-" * 50)


def main():
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()

            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Show strength
            strength = check_password_strength(password)
            print(f"Password strength: {strength}")

            # Confirm password
            confirm = input("Confirm password: ").strip()
            if password != confirm:
                print("Error: Passwords do not match.")
                continue

            # Register
            register_user(username, password)

        elif choice == '2':
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            if login_user(username, password):
                print("(In a real application, you would now access the dashboard.)")
                input("\nPress Enter to return to main menu...")

        elif choice == '3':
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__":
    # Optional: Create .gitignore entry for users.txt if needed
    if not os.path.exists(".gitignore"):
        with open(".gitignore", "w") as f:
            f.write("users.txt\n")

    main()


