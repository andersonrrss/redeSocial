from . import db

class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Usuário que recebeu a notficiação
    type = db.Column(db.String(50), nullable=False)  # Tipo da notificação ('new_follower', 'like', etc.)
    sender_id = db.Column(db.Integer, nullable=False)  # Usuário que originou a notificação (quem seguiu ou curtiu)
    post_id = db.Column(db.Integer, nullable=True)  # Se for 'like', armazena o ID do post
    view = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime)

    __table_args__ = (
        db.Index('idx_notifications_user_id', 'user_id'),
    )