from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Follower(db.Model):
    __tablename__ = 'followers'
    __table_args__ = {'extend_existing': True}
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

class Like(db.Model):
    __tablename__ = 'likes'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    socket_id = db.Column(db.Text, default=None)
    nome = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    profile_pic = db.Column(db.Text, nullable=False, default='/images/profile_pics/default.jpg')
    bio = db.Column(db.String(150), default='Olá! Tudo bem?')
    creation = db.Column(db.TIMESTAMP, default=datetime.now(timezone.utc))
    password_token = db.Column(db.String(32), nullable=False, unique=True)
    
    posts = db.relationship('Post', backref='user', lazy=True)

    # Relacionamento para obter os usuários que o usuário está seguindo
    following = db.relationship(
        'User', secondary='followers',
        primaryjoin=(Follower.follower_id == id),
        secondaryjoin=(Follower.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user1_deleted = db.Column(db.Boolean, default=False)
    user2_deleted = db.Column(db.Boolean, default=False)
    messages = db.relationship('Message', backref='chat', lazy=True)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    content = db.Column(db.String(1500))
    image_path = db.Column(db.Text)
    likes = db.relationship('Like', backref='post', lazy='dynamic')

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    parent_id = db.Column(db.Integer, default=0, nullable=False)
    content = db.Column(db.String(500))
    likes = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    view = db.Column(db.Boolean, default=False)
    parent_id = db.Column(db.Integer, default=0)
    user1_deleted = db.Column(db.Boolean, default=False)
    user2_deleted = db.Column(db.Boolean, default=False)

class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Usuário que recebeu a notficiação
    type = db.Column(db.String(50), nullable=False)  # Tipo da notificação ('new_follower', 'like', etc.)
    sender_id = db.Column(db.Integer, nullable=False)  # Usuário que originou a notificação (quem seguiu ou curtiu)
    post_id = db.Column(db.Integer, nullable=True)  # Se for 'like', armazena o ID do post
    view = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

# Criar índices
db.Index('idx_follower_user_id', Follower.followed_id)
db.Index('idx_follower_follower_id', Follower.follower_id)

db.Index('idx_like_user_id', Like.user_id)
db.Index('idx_like_post_id', Like.post_id)

db.Index('idx_users_id', User.id)
db.Index('idx_user_socket_id', User.socket_id)
db.Index('idx_nome', User.nome)
db.Index('idx_email', User.email)
db.Index('idx_senha', User.senha_hash)

db.Index('idx_chat_id', Chat.id)
db.Index('idx_chats_user1_deleted', Chat.user1_deleted)
db.Index('idx_chats_user2_deleted', Chat.user2_deleted)

db.Index('idx_posts_id', Post.id)
db.Index('idx_posts_user_id', Post.user_id)

db.Index('idx_comments_id', Comment.id)
db.Index('idx_comments_post_id', Comment.post_id)

db.Index('idx_messages_id', Message.id)
db.Index('idx_messages_chat_id', Message.chat_id)
db.Index('idx_messages_sender_id', Message.sender_id)
db.Index('idx_messages_receiver_id', Message.receiver_id)

db.Index('idx_notifications_user_id', Notification.user_id)
