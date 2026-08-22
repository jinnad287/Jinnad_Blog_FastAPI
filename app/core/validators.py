import re
from app.core.exceptions import ValidationException

class PasswordValidator:
    @staticmethod
    def validate(password: str) -> None:
        if len(password) < 8:
            raise ValidationException("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValidationException("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationException("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', password):
            raise ValidationException("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationException("Password must contain at least one special character.")

class EmailValidator:
    @staticmethod
    def validate(email: str) -> None:
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValidationException("Invalid email format.")

class StringValidator:
    @staticmethod
    def validate_length(string: str, min_length: int = 1, max_length: int = 255) -> None:
        if not (min_length <= len(string) <= max_length):
            raise ValidationException(f"String length must be between {min_length} and {max_length} characters.")
    