import os
import hashlib
import hmac
from typing import Tuple

def _hash_password(password:str, salt:bytes) -> bytes:
    """Hash a password with the given salt using PBKDF2 HMAC SHA256."""
    return hashlib.pbkdf2_hmac('sha256', password.encode("utf-8"), salt, 100000)

def make_password_hash(password: str) -> str:
    """Generate a salted hash for the given password."""
    salt = os.urandom(16)  # Generate a random 16-byte salt
    dk = _hash_password(password, salt)
    return salt.hex() + ":" + dk.hex()

def check_password_hash(password: str, stored:str) -> bool:
    try:
        salt_hex, hash_hex = stored.split(":")
    except ValueError:
        return False
    salt = bytes.fromhex(salt_hex)
    expected = bytes.fromhex(hash_hex)
    test = _hash_password(password, salt)
    return hmac.compare_digest(test, expected)

def normalize_email(email: str) -> str:
    return (email or "").strip().lower()