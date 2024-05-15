import sqlite3
import re

from helpers import error, login_required
from flask import Flask, render_template, jsonify, redirect, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)
# Chave secreta
app.secret_key = 'a1b2c3'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Configura a sessão
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Expressão regular para verificar o formato do email
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


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
    return error("Pra fazer", 404)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    return render_template("search.html")


@app.route("/getUsers")
def getUser():
    query = request.args.get("query")

    with sqlite3.connect("data.db") as conn:
        db = conn.cursor()
        # Pega o nome dos usuários que mais parecem com o que foi digitado
        usernames = db.execute(
            "SELECT id, nome FROM users WHERE nome LIKE ? LIMIT 20", (query + "%",)).fetchall()

        return jsonify(usernames)


@app.route("/notifications")
@login_required
def notifications():
    return error("Pra fazer", 404)

# Mostra o usuário ou o perfil de algum outro usuário


@app.route("/<username>", methods=["GET", "POST"])
@login_required
def user(username):
    with sqlite3.connect("data.db") as conn:
        db = conn.cursor()
        result = db.execute(
            "SELECT * FROM users WHERE nome = ?", (username,)).fetchone()
        if result is None:
            return error("Página não encontrada", 404)
        bio = result[5].replace("\n", "<br>")
        user = {
            "id": result[0],
            "name": result[1],
            "profile_pic": result[4],
            "bio": bio,
            "followers": result[6],
            "following": result[7]
        }

        if not user["followers"]:
            user["followers"] = 0
        else:
            user["followers"] = len(user["followers"].split(","))
        if not user["following"]:
            user["following"] = 0
        else:
            user["following"] = len(user["following"].split(","))

    if user["id"] == session["user_id"]:
        return render_template("me.html", user=user)
    return render_template("user.html", user=user)

# Editar o perfil do usuário


@app.route("/edit")
def edit():
    with sqlite3.connect("data.db") as conn:
        db = conn.cursor()
        result = db.execute("SELECT * FROM users WHERE nome = ?",
                            (session["name"],)).fetchone()
        if result is None:
            return error("Ocorreu um erro!", 404)
        print(result)
        # Informações editáveis
        user = {
            "id": result[0],
            "name": result[1],
            "email": result[2],
            "profile_pic": result[4],
            "bio": result[5],
        }

    return render_template("edit.html", user=user)

## CHECAGEM DE INFORMAÇÕES DE INPUTS

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

        with sqlite3.connect("data.db") as conn:
            db = conn.cursor()
            names_results = db.execute(
                "SELECT nome FROM users WHERE nome = ?", (username,)).fetchone()
            # Checa se o nome existe
            if names_results is not None:
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
        
        with sqlite3.connect("data.db") as conn:
            db = conn.cursor()
            email_result = db.execute(
                "SELECT email,senha FROM users WHERE email = ?", (email,)).fetchone()
            # Checa se o email existe
            if email_result is not None:
                result["exists"] = True
        
    # Retorna para o javascript
    return jsonify(result)
 
@app.route("/checkPassword")
def checkPassword():
    name_email = request.args.get("identifier")
    senha = request.args.get("senha")
    searchFor = "nome"

    if name_email:
        name_email = name_email.strip().lower()

    if re.match(EMAIL_PATTERN, name_email):
        searchFor = "email"
    
    with sqlite3.connect("data.db") as conn:
        db = conn.cursor()
        result = db.execute(f"SELECT senha_hash FROM users WHERE {searchFor} = ? ", (name_email,)).fetchone()[0]

        if check_password_hash(result, senha):
            return jsonify(isRight = True)
    
    return jsonify(isRight = False)


## EDIÇÕES ##

# Atualiza o nome


@app.route("/updatename")
def updatename():
    username = request.args.get("name")
    if username:
        username = username.lower().strip()  # Garante que o nome esteja no padrão
        # Checa se o nome é válido
        if username.find(" ") <= 0 and len(username) >= 6:
            with sqlite3.connect("data.db") as conn:
                db = conn.cursor()
                # Atualiza o banco de dados e a sessão
                db.execute("UPDATE users SET nome = ? WHERE id = ?",
                           (username, session["user_id"]))
                session["name"] = username
                conn.commit()
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
    with sqlite3.connect("data.db") as conn:
        db = conn.cursor()
        # Atualiza o banco de dados
        db.execute("UPDATE users SET bio = ? WHERE id = ?",
                   (bio, session["user_id"]))
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

    with sqlite3.connect("data.db") as conn:
        db = conn.cursor()

        if request.method == "GET":
            # Pega a lista de ids de seguidores
            result = db.execute(
                "SELECT followers_ids FROM users WHERE nome = ?", (username,)).fetchone()
        else:
            # Pega a lista de ids de seguidos
            result = db.execute(
                "SELECT following_ids FROM users WHERE nome = ?", (username,)).fetchone()

        if result is None:
            return error("Algo deu errado", 500)

        # Checa se o usuário tem seguidores
        if not result[0]:
            return jsonify(has_follows=False)

        # Transforma a string em uma lista
        follows_ids = result[0].split(",")

        # Pega as informações necessárias dos seguidores ou seguidos
        results = db.execute("SELECT id,nome,profile_pic FROM users WHERE id IN ({})".format(
            ",".join(["?"] * len(follows_ids))), follows_ids).fetchall()

        # Converter follows_infos em uma lista de dicionários para facilitar a serialização
        follows_infos = [{"id": user[0], "nome": user[1],
                          "profile_pic": user[2]} for user in results]

    return jsonify(has_follows=True, follows_infos=follows_infos)

# Aceita ambos os métodos


@app.route("/follow", methods=["GET", "POST"])
@login_required
def follow():
    # Pega id do perfil independente do método
    profile_id = request.values.get("user")

    user_id = session["user_id"]  # Id do usuário

    with sqlite3.connect("data.db") as conn:
        db = conn.cursor()
        profile_infos = db.execute("SELECT nome,followers_ids FROM users WHERE id = ?", (
            profile_id,)).fetchone()  # Informações do perfil

        # Obtendo o nome de usuário e a lista de seguidores
        profile_name, followers_ids = profile_infos
        # Obtendo a lista de seguidos do usuário
        following_ids = db.execute(
            "SELECT following_ids FROM users WHERE id = ?", (user_id,)).fetchone()[0]

        # Convertendo a lista de seguidores e de seguidos para uma lista
        followers_list = followers_ids.split(",") if followers_ids else []
        following_list = following_ids.split(",") if following_ids else []

        # Se o perfil não for seguido então o método recebido é GET
        if request.method == "GET":
            # Adicionando o novo seguidor à lista de seguidores do perfil
            followers_list.append(str(user_id))
            # Adicionando o novo seguido à lista de seguidos do usuário
            following_list.append(str(profile_id))
        # Se já seguir então é post
        else:
            # Verificando se o usuário está na lista de seguidores
            if str(user_id) in followers_list:
                # Removendo o usuário da lista de seguidores
                followers_list.remove(str(user_id))
                # Removendo o perfil da lista de seguidos do usuário
                following_list.remove(str(profile_id))

        # Atualiza a tabela com a nova lista de seguidores do perfil
        db.execute("UPDATE users SET followers_ids = ? WHERE id = ?",
                   (",".join(followers_list), profile_id))
        # Atualiza a tabela com a nova lista de seguidos do usuário
        db.execute("UPDATE users SET following_ids = ? WHERE id = ?",
                   (",".join(following_list), user_id))

        conn.commit()

        # Retorna que o usuário foi seguido
        return redirect(f"/{profile_name}")


@app.route("/isFollowed")
def isFollowed():
    # Pega o id fornecido pelo fetch
    profile_id = request.args.get("user")
    # Se conecta ao banco de dados
    with sqlite3.connect("data.db") as conn:
        db = conn.cursor()
        # Pega a lista de ids de seguidores do perfil

        followers_list = db.execute(
            "SELECT followers_ids FROM users WHERE id = ?", (profile_id,)).fetchone()[0]
        # Checa se existe uma lista de seguidores
        if not followers_list:
            return jsonify(is_followed=False)
        followers_list = followers_list.split(",")
        # Checa se o usuário está na lista e segue o perfil
        if str(session["user_id"]) in followers_list:
            return jsonify(is_followed=True)
    return jsonify(is_followed=False)


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

        with sqlite3.connect("data.db") as conn:
            db = conn.cursor()

            if re.match(EMAIL_PATTERN, name_email):
                result = db.execute(
                    "SELECT id, nome, senha_hash FROM users WHERE email = ?", (name_email,)).fetchone()
                if result is None:
                    return error("Email não cadastrado")
            else:
                result = db.execute(
                    "SELECT id, nome, senha_hash FROM users WHERE nome = ?", (name_email,)).fetchone()
                if result is None:
                    return error("Nome de usuário não encontrado")

            user = {
                "id": result[0],
                "name": result[1],
                "senha_hash": result[2]
            }

            if not check_password_hash(user["senha_hash"], senha):
                return error("Senha incorreta")

            session["user_id"] = user["id"]
            session["name"] = user["name"]

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

        with sqlite3.connect("data.db") as conn:
            db = conn.cursor()

            checkName = db.execute(
                "SELECT nome FROM users WHERE nome = ?", (username,)).fetchone()
            checkEmail = db.execute(
                "SELECT email FROM users WHERE email = ?", (email,)).fetchone()

            if checkName is not None:
                return error("Nome de usuário já cadastrado", 400)
            if checkEmail is not None:
                return error("Email já cadastrado", 400)

            db.execute("INSERT INTO users (nome,email,senha_hash) VALUES (?,?,?)",
                       (username, email, generate_password_hash(senha)))
            conn.commit()

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
    app.run()
