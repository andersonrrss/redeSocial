from flask import render_template, redirect, session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from models import db, Chat, Message

# Arquivos permitidos nos posts
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Erro
def error(message, code=400):
    return render_template("error.html", code=code, message=message), code

# Verifica se o usuário fez login
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


# Deleta o chat para o usuário
def delete_chat_for_user(chat_id, user_id):
    chat = Chat.query.get(chat_id) #id do chat
    messages = Message.query.filter_by(chat_id=chat_id).all() # mensagens do chat
    # Deleta o chat para o usuário que quis deletá-lo
    if chat.user1_id == user_id:
        chat.user1_deleted = True
        # Deleta todas as mensagens do chat para o usuário 1
        for message in messages:
            message.user1_deleted = True
    elif chat.user2_id == user_id:
        chat.user2_deleted = True
        # Deleta todas as mensagens do chat para o usuário 2
        for message in messages:
            message.user2_deleted = True

    if chat.user1_deleted and chat.user2_deleted:
        # Se ambos os usuários excluíram o chat, exclua o chat e suas mensagens
        Message.query.filter_by(chat_id=chat_id).delete()
        Chat.query.filter_by(id=chat_id).delete()
        db.session.delete(chat)
    db.session.commit()

# Carrega as mensagens do chat
def get_messages_for_chat(chat_id, user_id):
    chat = Chat.query.get(chat_id)
    if chat.user1_id == user_id:
        # Retorna apenas as mensagens que não foram deletadas pelo usuário 1
        return Message.query.filter(
            (Message.chat_id == chat_id) & (Message.user1_deleted == False)
        ).all()
    elif chat.user2_id == user_id:
        # Retorna apenas as mensagens que não foram deletadas pelo usuário 2
        return Message.query.filter(
            (Message.chat_id == chat_id) & (Message.user2_deleted == False)
        ).all()