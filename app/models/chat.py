from . import db

class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user1_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user1_deleted = db.Column(db.Boolean, default=False)
    user2_deleted = db.Column(db.Boolean, default=False)
    messages = db.relationship("Message", backref="chat", lazy=True)

    __table_args__ = (
        db.Index('idx_chat_id', 'id'),
        db.Index('idx_chats_user1_deleted', 'user1_deleted'),
        db.Index('idx_chats_user2_deleted', 'user2_deleted'),
    )