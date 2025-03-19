from . import db

class Like(db.Model):
    __tablename__ = 'likes'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)

    __table_args__ = ( 
        db.Index('idx_like_user_id', 'user_id'),
        db.Index('idx_like_post_id', 'post_id')
    )