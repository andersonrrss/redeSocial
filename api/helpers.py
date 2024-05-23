from flask import render_template, redirect, session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


def error(message, code=400):

    return render_template("error.html", code=code, message=message), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
