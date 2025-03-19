from flask import Blueprint, session, request
from app.models import User, db
from app import socketio

socketio_bp = Blueprint('socketio', __name__)

# Conecta o usuário
@socketio.on("connect")
def handle_connect():
    user_id = session.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.socket_id = request.sid  # Atualiza o SId do usuário
        db.session.commit()
        print(f"user {user_id} connected!!!")

# Desconecta o usuário
@socketio.on("disconnect")
def handle_disconnect():
    user_id = session.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.socket_id = None  # Retira o SId do usuário
        db.session.commit()
        print(f"User {user_id} disconnected\n")
