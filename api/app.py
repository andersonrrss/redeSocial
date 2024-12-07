import os
import re
import string
import secrets

from datetime import datetime, timezone
from flask import Flask, render_template, jsonify, redirect, request, session, url_for
from flask_migrate import Migrate
from flask_session import Session
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from helpers import allowed_file, error, login_required, delete_chat_for_user, get_messages_for_chat
from models import db, User, Message, Notification, Comment, Post, Chat, Follower, Like
from PIL import Image, ExifTags
from sqlalchemy import desc, and_
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

# Certifica que a pasta de uploads existe
os.makedirs("api/static/images/posts", exist_ok=True)

# Configurações da aplicação
app = Flask(__name__)
app.config.from_pyfile("config.py")
# Banco de dados
db.init_app(app)
# Sessão
Session(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Inicializa a migração 
migrate = Migrate(app, db)


# Expressão regular para verificar o formato do email
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

is_development = os.environ.get('FLASK_ENV') == 'development'

# Conecta o usuário
@socketio.on("connect")
def handle_connect():
    user_id = session.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.socket_id = request.sid # Atualiza o SId do usuário
        db.session.commit()

        print(f"user {user_id} connected!!!")

# Desconecta o usuário
@socketio.on('disconnect')
def handle_disconnect():
    user_id = session.get("user_id")
    user = User.query.filter_by(id=user_id)
    if user:
        user.socket_id = None # Retira o SId do usuário
        db.session.commit()

        print(f"User {user_id} disconnected\n")


@app.route("/")
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

# Adicionar uma nova publicação
@app.route("/add", methods=["POST", "GET"])
@login_required
def add():
    # Método POST se responsabiliza por adicionar o novo POST ao banco de dados
    if request.method == "POST":
        text = request.values.get("text")
        image = request.files['image']
        if text or image:
            if not text or len(text.strip()) == 0:
                text = "" # Garante que text seja None se o usuário não digitar nada

            # Cria o novo post
            new_post = Post(
                user_id = session.get("user_id"),
                content = text,
            )
            db.session.add(new_post)
            db.session.commit()
        
            if image:
                image_name = secure_filename(image.filename) # Nome da imagem
                if allowed_file(image_name):
                    ext = image_name.rsplit('.', 1)[1].lower() # Extrai a extensão da imagem
                    new_image_name = f"{new_post.id}.{ext}" # Renomeia a imagem com o id do post

                    # Abre a imagem
                    img = Image.open(image)

                    # Corrige a orientação da imagem se houver informações EXIF
                    try:
                        for orientation in ExifTags.TAGS.keys(): # Percorre as chaves dos metadados EXIF para encontrar a orientação
                            if ExifTags.TAGS[orientation] == 'Orientation': # Identifica o código da orientação
                                break # Interrompe o loop quando encontra a chave da orientação

                        exif = img._getexif() # Obtém os metadados EXIF da imagem
                        if exif is not None: # Verifica se a imagem possui metadados EXIF
                            orientation = exif.get(orientation, None) # Obtém o valor da orientação, se disponível

                            if orientation == 3:
                                img = img.rotate(180, expand=True)  # Rotaciona a imagem em 180 graus
                            elif orientation == 6:
                               img = img.rotate(270, expand=True)  # Rotaciona a imagem em 270 graus (90 graus no sentido horário)
                            elif orientation == 8:
                                img = img.rotate(90, expand=True)  # Rotaciona a imagem em 90 graus (90 graus no sentido anti-horário)
                    except (AttributeError, KeyError, IndexError):  # Captura possíveis erros ao acessar os metadados EXIF
                        # Se houver um erro ou a imagem não possuir EXIF, ignora a correção de orientação
                        pass
                    
                    # Converte e salva a imagem como PNG
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], new_image_name)
                    img.save(image_path, format="PNG", quality=90)  # Salva a imagem no formato PNG com qualidade alta
                    # Adiciona a imagem ao post
                    relative_image_path = f"images/posts/{new_image_name}" # Salvando apenas o caminho relativo ao static
                    new_post.image_path = relative_image_path
                else:
                    db.session.delete(new_post)
                    db.session.commit()
                    return error("Tipo de imagem não suportado, os tipos suportados são '.png', '.jpg', '.jpeg' e '.gif'", 400)
            else:
                # ISSO É REALMENTE NECESSÁRIO?
                image_path = None # Garante que o image path seja None se o usuário não colocou nenhuma imagem
            new_post.created_at = datetime.now(timezone.utc)
            db.session.commit()

            return redirect(f"/{session.get("name")}")
        
        else: 
            return error("Nenhuma imagem ou texto adicionados", 400)
        
    # Carrega a página para adicionar um novo post
    if "user_id" in session:
        user = db.session.get(User, session.get("user_id"))
        profile_pic = user.profile_pic
    return render_template("add.html", profile_pic=profile_pic)
    

@app.route("/chat")
@login_required
def chat():
    user_id = session.get("user_id")
    chats = []
    sugestions = []
    empty = True

    try:
        # Consulta para obter os chats em que o usuário está envolvido
        chats_results = Chat.query.filter(
            (Chat.user1_id == user_id) & (Chat.user1_deleted == False) |
            (Chat.user2_id == user_id) & (Chat.user2_deleted == False)
        ).all()
        chat_user_ids = set() # Armazena os ids de perfis que tenham chat vinculado com o usuário
        if chats_results:
            empty = False
            # Itera pelas conversas do usuário
            for chat in chats_results:
                receiver_id = chat.user1_id if chat.user2_id == user_id else chat.user2_id # O usuário que eu quero contatar
                receiver = User.query.get(receiver_id)
                chat_user_ids.add(receiver_id) # Armazena os ids dos perfis que já possuem um chat vinculado com o usuário
                # Organiza as informações
                chats.append({
                    "id": chat.id,
                    "receiver": {
                        "name": receiver.nome,
                        "profile_pic": receiver.profile_pic
                    },
                })
        # Pega seguidores do usuário para usar como sugestão e formata em uma lista
        following_ids = [follower.follower_id for follower in Follower.query.filter_by(followed_id=user_id).limit(15).all()]
        if following_ids:
            following_ids = [fid for fid in following_ids if fid not in chat_user_ids] # Exclui IDs dos usuários que já possuem um chat com o usuário atual
            result = User.query.filter(User.id.in_(following_ids)).all() # Solicita as informações necessárias dos usuários
            if result:
                empty = False
                # Organiza as sugestões
                for sugestion in result:
                    sugestions.append({
                        "id": sugestion.id, # O id vai ser usado para a criação de uma nova conversa
                        "name": sugestion.nome,
                        "profile_pic": sugestion.profile_pic
                    })
    except Exception as e:
        # Retorna uma resposta de erro
        return error(f"Erro ao carregar chats: {str(e)}", 500)
    
    return render_template("chat.html", chats=chats, sugestions=sugestions, empty=empty)

@app.route("/chat/<chat_id>")
@login_required
def chat_messages(chat_id):
    chat = Chat.query.filter_by(id=chat_id).first()
    user_id = session.get("user_id")
    if not chat:
        return error("Falha ao carregar conversa", 404)
    if chat.user1_id == user_id:
        receiver = User.query.filter_by(id=chat.user2_id).first()
    else:
        receiver = User.query.filter_by(id=chat.user1_id).first()

    # Usuário que vai receber minhas mensagens
    receiver = {
        "id": receiver.id,
        "socket_id": receiver.socket_id,
        "name": receiver.nome,
        "profile_pic": receiver.profile_pic,
    }
    messages_result = get_messages_for_chat(chat_id, user_id)
    messages = []
    new_messages = []
    for message in messages_result:
        parent_content = None
        if message.parent_id:
            reply = Message.query.get(message.parent_id)
            parent_content = reply.message
        
        message_data = {
            "timestamp":message.timestamp, 
            "content":message.message, 
            "sender_id":message.sender_id, 
            "message_id":message.id, 
            "parent_content": parent_content,
            "parent_id": message.parent_id,
            "received": False
        }
        if message.sender_id == session.get("user_id"):
            message.received = True

        if message.view:
            # Organiza as mensagens não lidas
            messages.append(message_data)
        else:
            if message.sender_id == receiver["id"]:
                # Organiza as mensagens não lidas
                new_messages.append(message_data)
                message.view = True # Atualizar o campo view para True nas mensagens novas
            else: 
                # Mensagens enviadas por mim
                messages.append(message_data)
    db.session.commit()

    chat = {
        "id": chat_id,
        "messages": messages,
        "new_messages": new_messages
    }

    return render_template("message.html", receiver=receiver, chat=chat)


@app.route("/deletechat", methods=["POST"])
@login_required
def delete_chat():
    chat_id = request.form.get("chat_id")
    user_id = session.get("user_id")
    if chat_id and user_id:
        delete_chat_for_user(chat_id, user_id)
        return redirect("/chat")
    else:
        return error("Algo deu errado", 500)
    
@app.route("/get_comments")
@login_required
def get_comments():
    post_id = request.args.get("post_id")
    comments = None
    return render_template("comments.html", comments=comments)


@app.route("/sendmessage")
@login_required
def send_message():
    chat_id = request.args.get("chat_id")
    receiver_id = request.args.get("receiver_id")
    message_content = request.args.get("message")
    sender_id = session.get("user_id")
    try: 
        parent_id = int(request.args.get("parent_id")) 
    except: 
        parent_id = 0

    new_message = Message(
        chat_id= chat_id,
        sender_id= sender_id,
        receiver_id= receiver_id,
        message= message_content,
        parent_id= parent_id, 
        timestamp= datetime.now(timezone.utc)
    )
    chat = Chat.query.get(chat_id)
    # Se algum usuário deletou o chat então ele será mostrado novamente
    if chat.user1_deleted:
        chat.user1_deleted = False

    if chat.user2_deleted:
        chat.user2_deleted = False
        
    db.session.add(new_message)
    db.session.commit()
    
    parent_message = None
    if parent_id != 0:
        parent_content = Message.query.filter_by(id=parent_id).first()
        parent_message = parent_content.message

    receiver_user = User.query.filter_by(id=receiver_id).first()
    sender_name = User.query.filter_by(id=new_message.sender_id).with_entities(User.nome).first()
    # Organiza as informações
    if receiver_user.socket_id:
        message_data = {
            "message_id": new_message.id,
            "content": message_content,
            "chat_id": new_message.chat_id,
            "sender_id": sender_id,
            "sender_name": sender_name[0],
            "timestamp": new_message.timestamp.isoformat(),
            "parent_message": parent_message,
            "parent_id": parent_id
        }
       
        # Emite a notificação
        socketio.emit("new-message", message_data, room=receiver_user.socket_id)

    return jsonify({"content":message_content, "message_id": new_message.id, "parent_message": parent_message, "parent_id": parent_id})


@app.route("/newchat")
@login_required
def newchat():
    user_id = session.get("user_id")
    receiver_id = request.args.get("receiver")
    chat = Chat.query.filter(
        (Chat.user1_id == user_id ) & (Chat.user2_id == receiver_id ) |
        (Chat.user1_id == receiver_id ) & (Chat.user2_id == user_id )
    ).first()
    if chat is not None:
        chat.user1_deleted = False
        chat.user2_deleted = False
    else:
        new_chat = Chat(user1_id=user_id, user2_id=receiver_id)
        db.session.add(new_chat)

    db.session.commit()
    try: 
        chat_id = new_chat.id
    except:
        chat_id = chat.id

    return redirect(f"/chat/{chat_id}")


@app.route("/messageviewed")
@login_required
def message_viewed():
    message_id = request.args.get("message_id")
    message = Message.query.filter_by(id=message_id).first()
    message.view = True
    db.session.commit()
    return "message view"


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    return render_template("search.html")


@app.route("/search_users")
def getUser():
    query = request.args.get("query")

    usernames = User.query.filter(User.nome.ilike(f"{query}%") & (User.id != session.get("user_id") )).limit(20).all() # Busca pelos nomes
    usernames = [user.nome for user in usernames] # Organiza as informações

    return jsonify(usernames)


@app.route("/notifications", methods=["GET", "POST"])
@login_required
def notifications():
    if request.method == "POST":
        user_id = session["user_id"]
        result = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).limit(20).all()

        if result is None:
            return jsonify([])
        notifications = []
        # Organiza as informações das notificações
        for notification in result:
            sender = User.query.filter_by(id=notification.sender_id).first()
            notifications.append({
                "senderName": sender.nome,
                "postId": notification.post_id,
                "type": notification.type,
                "viewed": notification.view,
                "timestamp": notification.timestamp
            })
            notification.view = True
        db.session.commit()
        # Retorna par o frontend
        return jsonify(notifications)

    return render_template("notifications.html")

# Mostra um post
@app.route("/post")
def post():
    post_id = request.args.get("id")
    post = Post.query.get(post_id)

    return render_template("post.html", post=post)

# Mostra o usuário ou o perfil de algum outro usuário


@app.route("/<username>")
@login_required
def user(username):
    result = User.query.filter_by(nome=username).first()
    if result is None:
        return error("Página não encontrada", 404)
    
    if result.posts:
        result.posts = sorted(result.posts, key=lambda post: post.created_at, reverse=True)
        for post in result.posts:
            print(post.created_at)
            post.content = post.content.replace("\n", "<br>") 
            post.like_count = post.likes.count() 
            like = Like.query.filter(Like.user_id == session.get("user_id"), Like.post_id == post.id).first()
            if like is not None:
                post.liked = True
            else:
                post.liked = False

    # Organiza o json para o javascript
    user = {
        "id": result.id,
        "followed": False,
        "follows_me": False,
        "socket_id": result.socket_id,
        "name": result.nome,
        "profile_pic": result.profile_pic,
        "bio": result.bio.replace("\n", "<br>"),
        "followers": result.followers.count(),
        "following": result.following.count(),
        "posts": result.posts,
        "its_me": result.id == session.get("user_id")
    }

    profile_id = user["id"]
    user_id = session.get("user_id") # ID do usuário(eu) 

    if(not user["its_me"]):
        # Checa se existe uma lista de seguidores
        if Follower.query.filter_by(followed_id=profile_id, follower_id=user_id).first():
            user["followed"] = True
        # Checa se existe uma lista de seguidos
        if Follower.query.filter_by(followed_id=user_id, follower_id=profile_id).first():
            user["follows_me"] = True

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
    username = request.values.get("username")  
    user = User.query.filter_by(nome=username).first()
    
    
    if not user:
        return error("Usuário não encontrado")
    
    # GET pede os seguidores
    if request.method == "GET":
        user_followers = user.followers.all()

        if not user_followers:
            return jsonify(has_follows=False)

        # Agora pega as informações dos seguidores diretamente
        followers_users = [{"id": u.id, "nome": u.nome, "email": u.email, "profile_pic": u.profile_pic} for u in user_followers]

        return jsonify(has_follows=True, follows_infos=followers_users)

    # POST pede os seguidos
    else:
        user_following = user.following.all()

        if not user_following:
            return jsonify(has_follows=False)
        
        # Agora pega as informações dos seguidos diretamente
        following_users = [{"id": u.id, "nome": u.nome, "email": u.email, "profile_pic": u.profile_pic} for u in user_following]

        return jsonify(has_follows=True, follows_infos=following_users)



@app.route("/follow")
@login_required
def follow():
    followed_id = request.values.get("user")
    user_id = session["user_id"]  # Id do usuário

    user = User.query.get(user_id)
    followed = User.query.get(followed_id)

    # Nome e socket_id do perfil a ser seguido
    followed_name, followed_socket = followed.nome, followed.socket_id
    
    # Verifica se a relação de seguimento já existe
    if user.following.filter_by(id=followed_id).first():
        return redirect(f"/{followed_name}")  # Redireciona sem fazer nada

    # Começar a seguir
    new_follower = Follower(followed_id=followed_id, follower_id=user_id)
    
    db.session.add(new_follower)
    new_notification = Notification(
        user_id=followed_id,
        sender_id=user_id,
        type= "new_follower",
        timestamp= datetime.now(timezone.utc)
        )
    # Verifica se a notificação já existe
    existing_notification = Notification.query.filter(
        and_(Notification.user_id == new_notification.user_id, Notification.sender_id == new_notification.sender_id, Notification.type == new_notification.type)
    ).first()
    if existing_notification:
        existing_notification.view = False
        existing_notification.timestamp = datetime.now(timezone.utc)
    else:
        db.session.add(new_notification)

    db.session.commit()
    if followed_socket is not None:
        # Envia a notificação de novo seguidor
        print(f"Sending notification to user {followed_id} at socket {followed_socket}")
        socketio.emit("new_follower", {
                      "follower_id": user_id, "follower_name": session["name"]}, room=followed_socket)
    
    # Retorna que o usuário foi seguido
    return redirect(f"/{followed_name}")

@app.route("/unfollow")
@login_required
def unfollow():
    profile_id = request.values.get("user")
    user_id = session["user_id"]

    profile = db.session.get(User, profile_id)
    
    if profile is None:
        return error("Algo deu errado", 404)
    
    if Follower.query.filter_by(followed_id=profile_id, follower_id=user_id).first():
        # Parar de seguir 
        Follower.query.filter_by(followed_id=profile_id, follower_id=user_id).delete()
        db.session.commit()

    # Recarrega a página
    return redirect(f"/{profile.nome}")
        
    
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


        if not check_password_hash(user.senha_hash, (senha + user.password_token)):
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

        characters = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(characters) for _ in range(32))

        senha_hash = generate_password_hash(senha+token)

        new_user = User(nome=username, email=email, senha_hash=senha_hash, password_token=token)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


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
    if user and check_password_hash(user.senha_hash, (senha+user.password_token)):
        return (jsonify(isRight=True))

    return jsonify(isRight=False)



@app.route("/logout")
@login_required
def logout():
    session.clear()

    return redirect("/login")

@app.route("/like")
@login_required
def like():
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
        print(f"contagem de likes do post {post_id} é {like_count}")
        return jsonify({"postId":post_id, "likeCount":like_count, "action":action})
    else:
        return jsonify({"error": "Algo deu errado"}), 404

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
    socketio.run(app, host='0.0.0.0', port=5000)