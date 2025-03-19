from flask import Blueprint, jsonify, render_template, request, session
from app.models import Notification, User, db
from app.helpers import login_required

notifications_bp = Blueprint("notifications", __name__)

def format_notification_data(notification, sender = None):
    return {
            "senderName": sender if sender else "Desconhecido",  # Adiciona um valor padrão
            "postId": notification.post_id,
            "type": notification.type,
            "viewed": notification.view,
            "timestamp": notification.timestamp
            }

@notifications_bp.route("/notifications", methods=["GET", "POST"])
@login_required
def notifications():
    if request.method == "POST":
        user_id = session["user_id"]
        result = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).limit(20).all()

        if result is None:
            return jsonify([])
        
        senders_ids = {notification.sender_id for notification in result}
        users = {user.id: user.name for user in User.query.filter(User.id.in_(senders_ids)).all()}

        notifications = [
            format_notification_data(notification, users.get(notification.sender_id)) 
            for notification in result
        ]

        # Atualiza a notificação para vista
        for notification in result:
            notification.view = True
        db.session.commit()
        # Retorna par o frontend
        return jsonify(notifications)

    return render_template("notifications.html")