from . import db
from sqlalchemy.sql import func

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=func.now())
    content = db.Column(db.String(1500))
    image_path = db.Column(db.Text)
    likes = db.relationship('Like', backref='post', lazy='dynamic')

    __table_args__ = (
        db.Index('idx_posts_id', 'id'),
        db.Index('idx_posts_user_id', 'user_id')
    )
