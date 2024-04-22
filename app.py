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


@app.route("/search")
@login_required
def search():
    return render_template("search.html")

@app.route("/notifications")
@login_required
def notifications():
    return error("Pra fazer", 404)

@app.route("/<username>")
@login_required
def user(username):
    user = {}
    if not username:
        username = session["name"]
    
    with sqlite3.connect("data.db") as conn:
        db = conn.cursor()
        result = db.execute("SELECT * FROM users WHERE nome = ?", (username,)).fetchone()
        if result is None:
            return error("Página não encontrada", 404)
        
        user = {
            "id": result[0],
            "name": result[1],
            "profile_pic": result[4],
            "bio": result[5],
            "followers": result[6],
            "following": result[7]
        }
        print(user)

        if not user["bio"]:
            user["bio"] = ""
        if not user["followers"]:
            user["followers"] = 0
        if not user["following"]:
            user["following"] = 0

    if user["id"] == session["user_id"]:
        return render_template("me.html", user=user)
    return render_template("user.html", user=user)
    

@app.route("/configs")
def configs():
    return render_template("configs.html")


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
            print(result)

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
