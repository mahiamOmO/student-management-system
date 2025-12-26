from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Add this to app/utils.py
def calculate_grade(marks: int):
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