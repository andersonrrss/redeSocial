from flask import Blueprint

from .auth import auth_bp
from .chat import chat_bp
from .main import main_bp
from .notification import notifications_bp
from .posts import posts_bp
from .search import search_bp
from .socketio import socketio_bp
from .user import user_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(socketio_bp)
    app.register_blueprint(user_bp)
    
