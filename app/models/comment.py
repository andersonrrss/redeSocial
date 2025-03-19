from . import db

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    parent_id = db.Column(db.Integer, default=None, nullable=True)
    content = db.Column(db.String(500))
    likes = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime)

    __table_args__ = (
        db.Index('idx_comments_id', 'id'),
        db.Index('idx_comments_post_id', 'post_id')
    )