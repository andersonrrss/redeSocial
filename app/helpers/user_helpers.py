from flask import session, redirect
from datetime import datetime, timezone
from sqlalchemy import and_
from app.models import User, Notification, Follower,db
from app.helpers import error

def load_follows(context, username):
    # Obtém o usuário com base no nome de usuário
    user = User.query.filter_by(name=username).first()

    if not user:
        return error("Usuário não encontrado")

    if context == "followers":
        # Verificando seguidores
        user_followers = user.followers.all()

        if not user_followers:
            return []

        followers_users = [{"id": u.id, "name": u.name, "profile_pic": u.profile_pic} for u in user_followers]
        return followers_users

    elif context == "following":
        # Verificando quem o usuário está seguindo
        user_following = user.following.all()

        if not user_following:
            return []

        following_users = [{"id": u.id, "name": u.name, "profile_pic": u.profile_pic} for u in user_following]
        return following_users

    else:
        return error("Contexto inválido")

def update_existing_notification(new_notification):
    # Verifica se a notificação já existe
    existing_notification = Notification.query.filter(
        and_(Notification.user_id == new_notification.user_id, Notification.sender_id == new_notification.sender_id, Notification.type == new_notification.type)
    ).first()
    if existing_notification:
        existing_notification.view = False
        existing_notification.timestamp = datetime.now(timezone.utc)
    else:
        db.session.add(new_notification)

def follow_user(follower_id, followed):
    # Verifica se a relação de seguimento já existe
    if Follower.query.filter_by(followed_id=followed.id, follower_id=follower_id).first():
        return redirect(f"/{followed.name}")

    new_follower = Follower(followed_id=followed.id, follower_id=follower_id)
    db.session.add(new_follower)
    
    new_notification = Notification(
        user_id=followed.id,
        sender_id=follower_id,
        type= "new_follower",
    )

    update_existing_notification(new_notification)
    db.session.commit()

    from app import socketio
    
    # Envia a notificação de novo seguidor se o socketId estiver disponível
    if followed.socket_id:
        socketio.emit("new_follower", {
                      "follower_id": follower_id, 
                      "follower_name": session["name"]
                      }, room=followed.socket_id)
    
    return redirect(f"/{followed.name}")

def unfollow_user(follower_id, followed):
    existing_following = Follower.query.filter_by(followed_id=followed.id, follower_id=follower_id).first()
    if existing_following:
        # Parar de seguir 
        Follower.query.filter_by(followed_id=followed.id, follower_id=follower_id).delete()
        db.session.commit()

    return redirect(f"/{followed.name}")