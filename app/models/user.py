from . import db
from .follower import Follower

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    socket_id = db.Column(db.Text, default=None)
    name = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_pic = db.Column(db.Text, nullable=False, default='/images/profile_pics/default.jpg')
    bio = db.Column(db.String(150), default='Olá! Tudo bem?')
    creation = db.Column(db.TIMESTAMP)
    password_token = db.Column(db.String(32), nullable=False, unique=True)

    posts = db.relationship("Post", backref="user", lazy=True)

    following = db.relationship("User",
        secondary="followers",
        primaryjoin=id == Follower.follower_id,
        secondaryjoin=id == Follower.followed_id,
        lazy="dynamic",
        back_populates='followers'
    )
                             

    followers = db.relationship("User",
        secondary="followers",
        primaryjoin=id == Follower.followed_id,
        secondaryjoin=id == Follower.follower_id,
        lazy="dynamic",
        back_populates='following'
    )


    __table_args__ = (
        db.Index('idx_users_id', 'id'),
        db.Index('idx_user_socket_id', 'socket_id'),
        db.Index('idx_name', 'name'),
        db.Index('idx_email', 'email'),
        db.Index('idx_password', 'password_hash')
    )