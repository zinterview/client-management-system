"""Authentication module."""
from functools import wraps

from flask import session, redirect

from app import CURRENT_USER_SESSION_KEY


def is_authenticated(func):
    """Decorator to check if request is authenticated."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if CURRENT_USER_SESSION_KEY in session:
            return func(*args, **kwargs)
        else:
            return redirect('/')
    return wrapper
