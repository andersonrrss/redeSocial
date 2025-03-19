from flask import Blueprint, render_template, session, request, jsonify
from app.helpers import login_required, error, load_follows, follow_user, unfollow_user
from app.models import User, Follower, db
user_bp = Blueprint('user', __name__)

@user_bp.route("/<username>")
@login_required
def user(username):
    result = User.query.filter_by(name=username).first()
    if result is None:
        return error("Página não encontrada", 404)
    
    user_id = session.get("user_id")  # ID do usuário logado

    # Checa se é o próprio perfil
    its_me = (result.id == user_id)

    followed = Follower.query.filter_by(followed_id=result.id, follower_id=user_id).first() is not None
    follows_me = Follower.query.filter_by(followed_id=user_id, follower_id=result.id).first() is not None
    # Organiza o json para o javascript
    user = {
        "id": result.id,
        "name": result.name,
        "profile_pic": result.profile_pic,
        "bio": result.bio,
        "followers_count": result.followers.count() or 0,
        "following_count": result.following.count() or 0,
        "its_me": its_me,
        "followed": followed,
        "follows_me": follows_me,
        "socket_id": result.socket_id,
    }

    return render_template("user/user.html", user=user)


@user_bp.route("/edit_profile")
def edit():
    user = User.query.filter_by(id=session["user_id"]).first()
    # Informações editáveis
    user = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "profile_pic": user.profile_pic,
        "bio": user.bio,
    }
    return render_template("user/edit.html", user=user)


@user_bp.route("/<username>/followers")
def followers(username):
    followers = load_follows("followers", username)
    return render_template("user/followers.html", profile_name=username, followers=followers)


@user_bp.route("/<username>/following")
def following(username):
    following = load_follows("following", username)
    return render_template("user/following.html", profile_name=username, followings=following)

@user_bp.route("/follow_unfollow", methods=["POST"])
@login_required
def follow_unfollow():
    action = request.values.get("action")
    target_user_id = request.values.get("user")
    current_user_id = session["user_id"]  # Id do usuário

    # Verifica se o usuário está tentando seguir a si mesmo
    if current_user_id == target_user_id:
        return error("Você não pode seguir a si mesmo")

    target_user = User.query.get(target_user_id)
    
    if not target_user:
        return error("usuário não encontrado", 404)
    
    if action == "follow":
        return follow_user(current_user_id, target_user)
    elif action == "unfollow":
        return unfollow_user(current_user_id, target_user)
    else:
        return error("Ação inválida")