#!/usr/bin/env python3
"""encrypt_password module."""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
    password (str): The password to hash.

    Returns:
    bytes: The salted, hashed password.
    """
    # Generate a salted, hashed password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password
