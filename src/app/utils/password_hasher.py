"""Module containing util for hashing and verifying passwords."""
import bcrypt


class PasswordHasher:
    """Class for hashing and verifying passwords."""

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash a password."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        """Check a plain text password against a hashed password."""
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
