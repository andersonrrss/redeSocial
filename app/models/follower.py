from . import db

class Follower(db.Model):
    __tablename__ = "followers"
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

    __table_args__ = (
        db.Index('idx_followed_id', 'followed_id'),
        db.Index('idx_follower_id', 'follower_id')
    )