import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from booking_engine import ALLOWED_EXTENSIONS

# Borrowing this code 'login_required' from cs50x course, week9 problem set Finance
# Becouse is very handy and i like it :D thanks!
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("admin_id") is None:
            return redirect("/admin_login")
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename: str):

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
