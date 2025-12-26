from passlib.context import CryptContext

# Setup password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """
    Hashes a plain text password using bcrypt.
    bcrypt supports max 72 bytes, so we truncate safely.
    """
    if not password:
        raise ValueError("Password cannot be empty")

    password = password.strip()     # remove whitespace
    password = password[:72]        # bcrypt max limit

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """
    Verifies a plain text password against its hashed version.
    """
    plain_password = plain_password.strip()
    plain_password = plain_password[:72]

    return pwd_context.verify(plain_password, hashed_password)


def calculate_grade(marks: int):
    """Automatically returns a grade based on UAP grading system."""
    if marks >= 80: return "A+"
    elif marks >= 75: return "A"
    elif marks >= 70: return "A-"
    elif marks >= 65: return "B+"
    elif marks >= 60: return "B"
    elif marks >= 55: return "B-"
    elif marks >= 50: return "C+"
    elif marks >= 45: return "C"
    elif marks >= 40: return "D"
    else: return "F"
