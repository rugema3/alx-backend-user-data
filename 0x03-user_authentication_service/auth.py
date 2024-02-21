#!/usr/bin/env python3
"""Define _hash_password method."""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes the input password using bcrypt.hashpw

    Args:
        password (str): The input password string to be hashed.

    Returns:
        bytes: The salted hash of the input password.
    """
    # Generate a salt using bcrypt.gensalt()
    salt = bcrypt.gensalt()

    # Hash the input password with the generated salt using bcrypt.hashpw()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    # Return the salted hash of the input password
    return hashed_password
