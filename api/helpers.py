from flask import render_template, redirect, session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Chat, Message


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

def delete_chat_for_user(chat_id, user_id):
    chat = Chat.query.get(chat_id)
    messages = Message.query.filter_by(chat_id=chat_id).all()
    if chat.user1_id == user_id:
        chat.user1_deleted = True
        for message in messages:
            message.user1_deleted = True
    elif chat.user2_id == user_id:
        chat.user2_deleted = True
        for message in messages:
            message.user2_deleted = True

    if chat.user1_deleted and chat.user2_deleted:
        # Se ambos os usuários excluíram o chat, exclua o chat e suas mensagens
        Message.query.filter_by(chat_id=chat_id).delete()
        Chat.query.filter_by(id=chat_id).delete()
        db.session.delete(chat)
    db.session.commit()

def get_messages_for_chat(chat_id, user_id):
    chat = Chat.query.get(chat_id)
    if chat.user1_id == user_id:
        return Message.query.filter(
            (Message.chat_id == chat_id) & (Message.user1_deleted == False)
        ).all()
    elif chat.user2_id == user_id:
        return Message.query.filter(
            (Message.chat_id == chat_id) & (Message.user2_deleted == False)
        ).all()