import string
import secrets
import logging

from flask import Blueprint, session, render_template, request, redirect, jsonify
from werkzeug.security import generate_password_hash
from app.helpers import check_email, check_username, check_password, error, validate_name_or_email, login_required, validate_password
from app.models import db, User

# Configura o logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("auth/register.html")
    
    try:
        username = request.form.get("username").strip().lower()
        email = request.form.get("email").strip().lower()
        password = request.form.get("password").strip()
        confirmation = request.form.get("confirmation").strip()

        username_result, username_error_message = check_username(username)
        email_result, email_error_message = check_email(email)
        password_result, password_error_message = check_password(password)

        if not username_result:
            return error(username_error_message, 400)
        if not email_result:
            return error(email_error_message, 400)
        if not password_result:
            return error(password_error_message, 400)

        if not confirmation:
            return error("Confirme sua senha", 400)
        if password != confirmation:
            return error("As senhas não coincidem", 400)

        characters = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(characters) for _ in range(32))
        password_hash = generate_password_hash(password+token)

        new_user = User(name=username, email=email, password_hash=password_hash, password_token=token)

        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    except Exception as e:
        # Log do erro para depuração
        logger.error(f"Erro durante o registro: {e}", exc_info=True)
        
        # Redireciona o usuário para a página de registro com uma mensagem de erro
        return error("Ocorreu um erro durante o registro. Tente novamente.", 500)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    
    try:
        session.clear()

        name_email = request.form.get("name-email", "").strip().lower()
        password = request.form.get("password", "").strip()

        validation_name_email, result = validate_name_or_email(name_email)
        if not validation_name_email:
            return error(result, 400)

        validation_password, password_result = validate_password(password, name_email)
        if not validation_password:
            return error(password_result, 400)

        session["user_id"] = result.id
        session["name"] = result.name

        return redirect("/")
    except Exception as e:
        # Log do erro para depuração
        logger.error(f"Erro durante o login: {e}", exc_info=True)
        
        # Redireciona o usuário para a página de login com uma mensagem de erro
        return error("Ocorreu um erro durante o login. Tente novamente.", 500)
    
@auth_bp.route("/checkUsername")
def checkname():
    username = request.args.get("username")
    result, message = check_username(username)
    return jsonify(result=result, message=message)

@auth_bp.route("/checkEmail")
def checkemail():
    email = request.args.get("email").strip()
    result, message = check_email(email)
    return jsonify(result=result, message=message)

@auth_bp.route("/checkPassword")
def checkPassword():
    password = request.args.get("password").strip()
    result, message = check_password(password)
    return jsonify(result=result, message=message)

@auth_bp.route("/validateNameOrEmail")
def validateNameOrEmail():
    nameOrEmail = request.args.get("nameOrEmail").strip()
    result, message = validate_name_or_email(nameOrEmail)
    if isinstance(message, str):
        return jsonify(result=result, message=message)
    return jsonify(result=result, message="")

@auth_bp.route("/validatePassword", methods=["POST"])
def validatePassword():
    data = request.get_json() 
    password = data.get("password", '').strip()
    info = data.get("info", "").strip()

    result, message = validate_password(password, info)
    return jsonify(result=result, message=message)

@auth_bp.route("/logout")
@login_required
def logout():
    session.clear()

    return redirect("/login")