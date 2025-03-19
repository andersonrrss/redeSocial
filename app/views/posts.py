import os
import logging

from PIL import Image
from flask import Blueprint, jsonify, request, session, render_template, redirect
from werkzeug.utils import secure_filename
from app.config import Config
from app.models import User, Like, Post, db
from app.helpers import adjust_image_orientation ,login_required, get_user_posts, get_feed_posts, allowed_file, error

# Configura o logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

posts_bp = Blueprint("posts", __name__)

@posts_bp.route("/loadPosts")
def load_posts():
    try:
        user_id = session.get("user_id")
        # Contexto: 'user_posts' para posts de um único usuário, 'feed' para carregar posts no feed
        context = request.args.get('context', 'user_posts')

        page = request.args.get("page", 1, type=int)
        per_page = 10

        if context == 'user_posts':
            username = request.args.get("username")
            posts_paginated, error = get_user_posts(username, page, per_page)
            if error:
                return jsonify({"error": error}), 404
        elif context == 'feed':
            posts_paginated = get_feed_posts(user_id, page, per_page)
        else: 
            return jsonify({"error": "Contexto inválido"}), 400
        
        posts_data = [render_template('macros/post_macro.html', post=post) for post in posts_paginated]

        return jsonify({
            "posts": posts_data,
            "has_next": posts_paginated.has_next
        })

    except Exception as e:
        logger.error(f"Erro ao carregar posts: {e}")
        return jsonify({"error": str(e)}), 500
    

@posts_bp.route("/addPost", methods=["POST", "GET"])
@login_required
def addPost():
    if request.method == "GET":
        user = db.session.get(User, session.get("user_id"))
        profile_pic = user.profile_pic
        return render_template("posts/add.html", profile_pic=profile_pic)
    
    text = request.values.get("text", "").strip()
    image = request.files.get('image', None)

    if not text and not image:
        return error("Nenhuma imagem ou texto adicionados", 400)
    
    # Cria o novo post
    new_post = Post(
        user_id = session.get("user_id"),
        content = text,
    )
    
    db.session.add(new_post)
    db.session.commit()

    if image:
        image_name = secure_filename(image.filename) # Nome da imagem

        if not allowed_file(image_name):
            db.session.delete(new_post)
            db.session.commit()
            return error("Tipo de imagem não suportado, os tipos suportados são '.png', '.jpg', '.jpeg' e '.gif'", 400)

        ext = image_name.rsplit('.', 1)[1].lower() # Extrai a extensão da imagem
        new_image_name = f"{new_post.id}.{ext}" # Renomeia a imagem com o id do post

        # Abre a imagem
        with Image.open(image) as img:
            img = adjust_image_orientation(img)
            # Converte e salva a imagem como PNG
            image_path = os.path.join(Config.UPLOAD_FOLDER, new_image_name)
            img.save(image_path, format="PNG", quality=90)  # Salva a imagem no formato PNG com qualidade alta

        # Adiciona a imagem ao post
        relative_image_path = f"images/posts/{new_image_name}" # Salvando apenas o caminho relativo ao static
        new_post.image_path = relative_image_path
        
    db.session.commit()
    return redirect(f"/{session.get("name")}")

@posts_bp.route("/likePost")
@login_required
def likePost():
    post_id = request.args.get("post_id")
    user_id = session.get("user_id")
    if post_id:
        like = Like.query.filter(Like.user_id==user_id, Like.post_id==post_id).first()
        if not like:
            new_like = Like(user_id=user_id, post_id=post_id)
            db.session.add(new_like)
            action = "like"
        else:
            action = "dislike"
            db.session.delete(like)

        db.session.commit()

        like_count = Like.query.filter_by(post_id=post_id).count()

        return jsonify({"postId":post_id, "likeCount":like_count, "action":action})
    else:
        return jsonify({"error": "Algo deu errado"}), 404


@posts_bp.route("/get_comments")
@login_required
def get_comments():
    post_id = request.args.get("post_id")
    comments = None
    return jsonify({"Os comentários vão ser chamados com um fetch"})