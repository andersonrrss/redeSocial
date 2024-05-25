import re

from flask import Flask, render_template, jsonify, redirect, request, session
from flask_session import Session
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from helpers import error, login_required
from models import db, User, Message, Notification, Comment, Post, Chat
from werkzeug.security import check_password_hash, generate_password_hash


# Configure application
app = Flask(__name__)
app.config.from_pyfile("config.py")
# Banco de dados
db.init_app(app)
# Sessão
Session(app)
socketio = SocketIO(app, cors_allowed_origins="*")


# Expressão regular para verificar o formato do email
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


@socketio.on("connect")
def handle_connect():
    user_id = session.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.socket_id = request.sid
        db.session.commit()

        print(f"user {user_id} connected!!!")


@socketio.on('disconnect')
def handle_disconnect():
    user_id = session.get("user_id")
    user = User.query.filter_by(id=user_id)
    if user:
        user.socket_id = None
        db.session.commit()

        print(f"User {user_id} disconnected\n")


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/add")
@login_required
def add():
    return error("Pra fazer", 404)


@app.route("/chat")
@login_required
def chat():
    return render_template("chat.html", chats=None)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    return render_template("search.html")


@app.route("/getUsers")
def getUser():
    query = request.args.get("query")

    usernames = User.query.filter(User.nome.ilike(f"{query}%")).limit(20).all()
    usernames = [user.nome for user in usernames]

    return jsonify(usernames)


@app.route("/notifications", methods=["GET", "POST"])
@login_required
def notifications():
    if request.method == "POST":
        user_id = session["user_id"]
        result = Notification.query.filter_by(user_id=user_id).limit(20).all()

        if result is None:
            return jsonify([])
        notifications = []
        # Organiza as informações das notificações
        for notification in result:
            notifications.append({
                "content": notification.content,
                "notification_type": notification.notification_type,
                "viewed": notification.view,
                "timestamp": notification.timestamp
            })
            notification.view = True
        db.session.commit()
        # Retorna par o frontend
        return jsonify(notifications)

    return render_template("notifications.html")

# Mostra o usuário ou o perfil de algum outro usuário


@app.route("/<username>", methods=["GET", "POST"])
@login_required
def user(username):
    result = User.query.filter_by(nome=username).first()
    if result is None:
        return error("Página não encontrada", 404)
    # Organiza o json para o javascript
    user = {
        "id": result.id,
        "socket_id": result.socket_id,
        "name": result.nome,
        "profile_pic": result.profile_pic,
        "bio": result.bio.replace("\n", "<br>"),
        "followers": result.followers_ids,
        "following": result.following_ids
    }
    # Formata a quantiade de seguidores
    if user["followers"]:
        user["followers"] = len(user["followers"].split(","))
    else:
        user["followers"] = 0

    if user["following"]:
        user["following"] = len(user["following"].split(","))
    else:
        user["following"] = 0

    if user["id"] == session["user_id"]:
        return render_template("me.html", user=user)
    return render_template("user.html", user=user)

# Editar o perfil do usuário


@app.route("/edit")
def edit():
    user = User.query.filter_by(id=session["user_id"]).first()
    # Informações editáveis
    user = {
        "id": user.id,
        "name": user.nome,
        "email": user.email,
        "profile_pic": user.profile_pic,
        "bio": user.bio,
    }
    return render_template("edit.html", user=user)

# CHECAGEM DE INFORMAÇÕES DE INPUTS

# Checa a disponibilidade de um nome de usário


@app.route("/checkname")
def checkname():
    username = request.args.get("name")
    # Informações para o JS
    result = {
        "isValid": False,
        "exists": False
    }
    # Checa se o nome foi digitado
    if username is not None and username.strip():
        username = username.lower().strip()  # Deixa o nome no formato padrão

        # Checa se o nome é válido
        if username.find(" ") <= 0 and len(username) >= 6:
            result["isValid"] = True

        if User.query.filter_by(nome=username).first():
            result["exists"] = True
        # Retorna para o javascript

    return jsonify(result)

# Checagem do email


@app.route("/checkemail")
def checkemail():
    email = request.args.get("email")
    # Informações para o JS
    result = {
        "isValid": False,
        "exists": False,
    }

    if email is not None and email.strip():
        email = email.strip()
        # Checa se o email é válido
        if email.find(" ") <= 0 and re.match(EMAIL_PATTERN, email):
            result["isValid"] = True

        if User.query.filter_by(email=email).first():
            result["exists"] = True

    # Retorna para o javascript
    return jsonify(result)


@app.route("/checkPassword")
def checkPassword():
    name_email = request.args.get("identifier")
    senha = request.args.get("senha")

    if name_email:
        name_email = name_email.strip().lower()

    # pega as informações do usuário por nome ou email
    if re.match(EMAIL_PATTERN, name_email):
        user = User.query.filter_by(email=name_email).first()
    else:
        user = User.query.filter_by(nome=name_email).first()

    # Verifica a senha
    if user and check_password_hash(user.senha_hash, senha):
        return (jsonify(isRight=True))

    return jsonify(isRight=False)


## EDIÇÕES ##

# Atualiza o nome


@app.route("/updatename")
def updatename():
    username = request.args.get("name")
    if username:
        username = username.lower().strip()  # Garante que o nome esteja no padrão
        # Checa se o nome é válido
        if username.find(" ") <= 0 and len(username) >= 6:
            user = User.query.filter_by(id=session["user_id"]).first()
            if user:
                session["name"] = username
                user.nome = username
                db.session.commit()
            # Recarrega a página

            return redirect("/edit")
        else:
            return error("Ocorreu um erro", 500)

# Atualizar a bio do usuário


@app.route("/update_bio")
def update_bio():
    bio = request.values.get("bio")  # bio
    if bio:
        bio = bio.strip()  # Remove os espaços desnecessários
        user = User.query.filter_by(id=session["user_id"]).first()
        if user:
            user.bio = bio
            db.session.commit()
    # Recarrega a página
    return redirect("/edit")

# Seguidores do usuário


@app.route("/<username>/followers")
def followers(username):
    return render_template("followers.html", profile_name=username)

# Seguindo do usuário


@app.route("/<username>/following")
def following(username):
    return render_template("following.html", profile_name=username)


@app.route("/follows", methods=["GET", "POST"])
def follows():
    username = request.values.get("username")  # Nome do usuário
    if not username:
        return error("Algo deu errado", 404)

    result = User.query.filter_by(nome=username).first()
    if result is None:
        return error("Algo deu errado", 500)
    # GET pede os seguidores
    if request.method == "GET":
        # Checa se o usuário tem seguidores
        if not result.followers_ids:
            return jsonify(has_follows=False)
        # Transforma a string em uma lista
        follows_ids = result.followers_ids.split(",")
    # POST pede os seguidos
    else:
        # Checa se o usuário tem seguidores
        if not result.following_ids:
            return jsonify(has_follows=False)

        # Transforma a string em uma lista
        follows_ids = result.following_ids.split(",")
    follows = User.query.filter(User.id.in_(follows_ids)).with_entities(
        User.id, User.nome, User.profile_pic).all()
    # Converter follows_infos em uma lista de dicionários para facilitar a serialização
    follows_infos = [{"id": user.id, "nome": user.nome,
                      "profile_pic": user.profile_pic} for user in follows]

    return jsonify(has_follows=True, follows_infos=follows_infos)

# Aceita ambos os métodos


@app.route("/follow", methods=["GET", "POST"])
@login_required
def follow():
    # Pega id do perfil independente do método
    profile_id = request.values.get("user")
    user_id = session["user_id"]  # Id do usuário

    profile_infos = User.query.filter_by(id=profile_id).with_entities(
        User.nome, User.followers_ids, User.socket_id).first()

    # Obtendo o nome de usuário e a lista de seguidores
    profile_name, followers_ids, profile_socket = profile_infos.nome, profile_infos.followers_ids, profile_infos.socket_id
    if not profile_name:
        return error("Algo deu errado", 500)
    # Obtendo a lista de seguidos do usuário
    following_ids = User.query.filter_by(
        id=user_id).with_entities(User.following_ids).first()[0]

    # Convertendo a lista de seguidores e de seguidos para uma lista
    followers_list = followers_ids.split(",") if followers_ids else []
    following_list = following_ids.split(",") if following_ids else []

    # Se o perfil não for seguido então o método recebido é GET
    if request.method == "GET":
        # Atualizando o banco de dados
        followers_list.append(str(user_id))
        following_list.append(str(profile_id))
        # Envia notificação do novo seguidor para o perfil seguido
        new_notification = Notification(
            content=f"@{profile_name} começou a seguir você!", notification_type="follow", user_id=profile_id)
        db.session.add(new_notification)
        db.session.commit()

        if profile_socket is not None:
            # Envia a notificação de novo seguidor
            print(f"Sending notification to user {profile_id} at socket {profile_socket}")
            socketio.emit("new_follower", {
                          "follower_id": user_id, "follower_name": session["name"]}, room=profile_socket)

    # Se já seguir então é POST
    else:
        # Verificando se o usuário está na lista de seguidores
        if str(user_id) in followers_list:
            # Atualizando o banco de dados
            followers_list.remove(str(user_id))
            following_list.remove(str(profile_id))

    # Atualiza a tabela com a nova lista de seguidores do perfil
    followed = User.query.filter_by(id=profile_id).first()
    followed.followers_ids = ",".join(followers_list)
    # Atualiza a tabela com a nova lista de seguidos do usuário
    follower = User.query.filter_by(id=user_id).first()
    follower.following_ids = ",".join(following_list)

    db.session.commit()
    # Retorna que o usuário foi seguido
    return redirect(f"/{profile_name}")


@app.route("/isFollowed")
def isFollowed():
    # Pega o id fornecido pelo fetch
    profile_id = request.args.get("user")
    # Pega a lista de ids de seguidores e seguidos do perfil
    profile_infos = User.query.filter_by(
        id=profile_id).with_entities(User.followers_ids, User.following_ids).first()
    # Checa se existe uma lista de seguidores
    if profile_infos.followers_ids:
        followers_list = profile_infos.followers_ids.split(",")
        # Checa se eu já sigo o perfil
        if str(session["user_id"]) in followers_list:
            return jsonify(is_followed=True)
    # Checa se existe uma lista de seguidos
    if profile_infos.following_ids:
        following_list = profile_infos.following_ids.split(",")
        # Checa se o perfil já me segue
        if str(session["user_id"]) in following_list:
            return jsonify(is_followed=False, follows_me=True)

    return jsonify(is_followed=False, follows_me=False)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.clear()
        name_email = request.form.get("name-email").strip().lower()
        senha = request.form.get("senha").strip()

        if not name_email:
            return error("Digite seu nome de usuário ou seu email", 400)
        if not senha:
            return error("Digite sua senha")

        if re.match(EMAIL_PATTERN, name_email):
            user = User.query.filter_by(email=name_email).first()
        else:
            user = User.query.filter_by(nome=name_email).first()

        if not user:
            return error("Nome ou email incorretos", 400)

        if not check_password_hash(user.senha_hash, senha):
            return error("Senha incorreta", 400)

        session["user_id"] = user.id
        session["name"] = user.nome

        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").strip().lower()
        email = request.form.get("email").strip().lower()
        senha = request.form.get("senha").strip()
        confirmation = request.form.get("confirmation").strip()

        if not username:
            return error("Digite um nome de usuário", 400)
        if not email:
            return error("Digite um email", 400)
        if not senha:
            return error("Digite uma senha", 400)
        if not confirmation:
            return error("Confirme sua senha", 400)

        if len(username) < 6:
            return ("Seu nome de usuário deve conter pelo menos 6 caracteres", 400)
        # Verifica se o email corresponde ao padrão
        if not re.match(EMAIL_PATTERN, email):
            return error("Digite um email válido", 400)
        # Verifica se a senha tem pelo menos 8 caracteres
        if len(senha) < 8:
            return error("Sua senha deve conter pelo menos 8 caracteres", 400)
        if senha != confirmation:
            return error("As senhas não coincidem", 400)
        # Verifica se o nome ou email já estão cadastrados
        if User.query.filter_by(nome=username).first() is not None:
            return error("Nome de usuário já cadastrado", 400)
        if User.query.filter_by(email=email).first() is not None:
            return error("Email já cadastrado", 400)

        senha_hash = generate_password_hash(senha)

        new_user = User(nome=username, email=email, senha_hash=senha_hash)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()

    return redirect("/login")


@app.context_processor
def inject_user():
    username = None
    if "user_id" in session:
        username = session["name"]
    return dict(username=username)


if __name__ == "__main__":
    # Criar as tabelas no banco de dados
    with app.app_context():
        db.create_all()
    socketio.run(app)
