from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .chat import Chat
from .comment import Comment
from .follower import Follower
from .like import Like
from .message import Message
from .notification import Notification
from .post import Post
from .user import User