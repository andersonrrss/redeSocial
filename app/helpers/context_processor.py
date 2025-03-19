from flask import session

def inject_user():
    username = None
    if "user_id" in session:
        username = session.get("name")
    return dict(username=username)