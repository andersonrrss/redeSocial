from . import db

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    view = db.Column(db.Boolean, default=False)
    responded_message_id = db.Column(db.Integer, default=None, nullable=True)
    user1_deleted = db.Column(db.Boolean, default=False)
    user2_deleted = db.Column(db.Boolean, default=False)

    __table_args__ = (
        db.Index('idx_messages_id', 'id'),
        db.Index('idx_messages_chat_id', 'chat_id'),
        db.Index('idx_messages_sender_id', 'sender_id'),
        db.Index('idx_messages_receiver_id', 'receiver_id')
    )
