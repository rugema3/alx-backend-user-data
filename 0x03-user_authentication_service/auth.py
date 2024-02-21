#!/usr/bin/env python3
"""Define _hash_password method."""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


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


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user

        Args:
            email (str): The email of the user to register.
            password (str): The password of the user to register.

        Returns:
            User: The newly registered User object.

        Raises:
            ValueError: If a user already exists with the provided email.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            new_user = self._db.add_user(email, hashed)
            return new_user
        raise ValueError(f"User {email} already exists")
