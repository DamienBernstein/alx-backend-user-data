#!/usr/bin/env python3
"""
Defines functions for hashing and validating passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Returns a hashed password.
    Args:
        password (str): Password to be hashed.
    Returns:
        bytes: The hashed password.
    """
    password_bytes = password.encode()
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check whether a password is valid.
    Args:
        hashed_password (bytes): Hashed password.
        password (str): Password in string.
    Returns:
        bool: True if the password is valid, False otherwise.
    """
    password_bytes = password.encode()
    return bcrypt.checkpw(password_bytes, hashed_password)
