from flask import Blueprint, jsonify, request, session, render_template
from app.helpers import login_required
from app.models import User

search_bp = Blueprint("search", __name__)

@search_bp.route("/search", methods=["GET", "POST"])
@login_required
def search():
    return render_template("search.html")


@search_bp.route("/search_users")
def getUser():
    query = request.args.get("query")

    usernames = User.query.filter(User.name.ilike(f"{query}%") & (User.id != session.get("user_id") )).limit(20).all() # Busca pelos nomes
    usernames = [user.name for user in usernames] # Organiza as informações

    return jsonify(usernames)
