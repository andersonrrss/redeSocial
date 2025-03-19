from flask import Blueprint, render_template, session
from app.helpers import login_required
from app.models import User, Post, Follower, Like, db
from sqlalchemy import desc

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
@login_required
def index():
    user = User.query.filter_by(id=session.get("user_id")).first()

    # Subquery para encontrar os IDs dos perfis que o usuário segue
    seguindo_ids = db.session.query(Follower.followed_id).filter_by(follower_id=user.id).subquery()

    liked_posts = db.session.query(Like.post_id).filter_by(user_id=user.id).subquery()

    # Consulta os posts dos perfis que o usuário segue e que ele ainda não curtiu
    posts_nao_curtidos = Post.query.filter(
        Post.user_id.in_(seguindo_ids)  # Posts dos perfis seguidos
    ).filter(
        Post.id.notin_(liked_posts)  # Exclui posts já curtidos pelo usuário
    ).order_by(desc(Post.created_at)).limit(50).all()

    for post in posts_nao_curtidos:
        post.like_count = post.likes.count()
        post.content = post.content.replace("\n", "<br>")

    return render_template("index.html", posts=posts_nao_curtidos)
