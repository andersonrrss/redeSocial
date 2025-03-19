from flask import request, session
from PIL import ExifTags
from app.models import db, User, Like, Post

def get_user_posts(username, page, per_page):
    username = request.args.get("username")
    result = User.query.filter_by(name=username).first()
    
    if not result:
        return [], "Usuário não encontrado"
    posts_paginated = Post.query.filter_by(user_id=result.id).order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page)

    for post in posts_paginated.items:
        post.like_count = post.likes.count()  # Contagem de likes
        post.liked = Like.query.filter(Like.user_id == session.get("user_id"), Like.post_id == post.id).first() is not None

    return posts_paginated, None

def get_feed_posts(user_id, page, per_page):
    followed_users = [followed.id for followed in User.query.get(user_id).following]

    liked_posts_subquery = db.session.query(Like.post_id).filter_by(user_id=user_id).subquery()
    posts_paginated = Post.query.filter(
        Post.user_id.in_(followed_users), 
        Post.id.notin_(liked_posts_subquery)
    ).order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page)

    for post in posts_paginated.items:
        post.like_count = post.likes.count()  # Contagem de likes
        post.liked = Like.query.filter(Like.user_id == session.get("user_id"), Like.post_id == post.id).first() is not None

    return posts_paginated

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif',}

def adjust_image_orientation(img):
    """
    Corrige a orientação da imagem com base nos metadados EXIF.

    Args:
        img (PIL.Image): A imagem a ser ajustada.

    Returns:
        PIL.Image: A imagem ajustada com a orientação correta.
    """
    try:
        exif = img._getexif() # Obtém os metadados EXIF da imagem
        orientation_key = next((key for key, value in ExifTags.TAGS.items() if value == 'Orientation'), None)
        
        if exif is None or orientation_key is None: # Verifica se a imagem possui metadado EXIF ou se possui metadados de rotação
            return img
        
        orientation = exif.get(orientation_key, None) # Obtém o valor da orientação, se disponível
        orientation_map = {
            3: 180,
            6: 270,
            8: 90
        }

        if orientation in orientation_map:
            return img.rotate(orientation_map[orientation], expand=True)
        
    except (AttributeError, KeyError, IndexError):  # Captura possíveis erros ao acessar os metadados EXIF
        # Se houver um erro ou a imagem não possuir EXIF, ignora a correção de orientação
        return img
    return img