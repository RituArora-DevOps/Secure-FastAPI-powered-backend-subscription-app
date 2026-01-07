from passlib.context import CryptContext

# one shared hashing context for the whole app
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password for storage. Return a secure hash for the given plain-text password."""
    return _pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a stored password against one provided by user"""
    return _pwd_context.verify(plain_password, hashed_password)