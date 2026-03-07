import re

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> bool:
    return len(password) >= 8

def validate_username(username: str) -> bool:
    return 3 <= len(username) <= 20

def validate_phone(phone: str) -> bool:
    pattern = r'^1[3-9]\d{9}$'
    return re.match(pattern, phone) is not None if phone else True
