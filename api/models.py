from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    socket_id = db.Column(db.Text, default=None)
    nome = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    profile_pic = db.Column(db.Text, nullable=False, default='/images/profile/default.jpg')
    bio = db.Column(db.String(150), default='Olá! Tudo bem?')
    followers_ids = db.Column(db.Text)
    following_ids = db.Column(db.Text)
    creation = db.Column(db.TIMESTAMP, default=datetime.utcnow)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    image_path = db.Column(db.Text)
    likes_ids = db.Column(db.Text)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    parent_id = db.Column(db.Integer, default=0, nullable=False)
    content = db.Column(db.String(500))
    likes = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    view = db.Column(db.Boolean, default=False)
    parent_id = db.Column(db.Integer, default=0)

class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)
    view = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Criar índices
db.Index('idx_users_id', User.id)
db.Index('idx_user_socket_id', User.socket_id)
db.Index('idx_nome', User.nome)
db.Index('idx_email', User.email)
db.Index('idx_senha', User.senha_hash)

db.Index('idx_posts_id', Post.id)
db.Index('idx_posts_user_id', Post.user_id)

db.Index('idx_comments_id', Comment.id)
db.Index('idx_comments_post_id', Comment.post_id)

db.Index('idx_messages_id', Message.id)
db.Index('idx_messages_sender_id', Message.sender_id)
db.Index('idx_messages_receiver_id', Message.receiver_id)

db.Index('idx_notifications_user_id', Notification.user_id)
