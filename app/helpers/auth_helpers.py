import re
import unicodedata

from flask import render_template, redirect, session
from functools import wraps
from werkzeug.security import check_password_hash
from ..models import db, User
from .error import error

def normalize_username(username):
    # Normaliza a string para a forma NFKD (decomposição compatível)
    username = unicodedata.normalize("NFKD", username)
    
    # Remove caracteres não ASCII (como acentos)
    username = username.encode("ascii", "ignore").decode("ascii")
    
    username = username.strip().lower()

    return username

# Expressão regular para verificar o formato do email
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def check_username(username):
    username = normalize_username(username)
    print(username)
    if not username:
        return False, "Digite um nome de usuário"
    if len(username) < 6:
        print("pequeno")
        return False, "Seu nome de usuário deve conter pelo menos 6 caracteres"
    if len(username) > 45:
        return False, "Seu nome de usuário deve conter no máximo 45 caracteres"
    if " " in username:
        return False, "Seu nome de usuário não pode conter espaços"
    if User.query.filter_by(name=username).first() is not None:
        return False, "Nome de usuário já cadastrado"
    
    return True, ""

def check_email(email):
    email = email.strip().lower()

    if not email:
        return False, "Digite um email"
    if not re.match(EMAIL_PATTERN, email):
        return False, "Seu email não é válido"
    if User.query.filter_by(email=email).first() is not None:
        return False, "Email já cadastrado"

    return True, ""

def check_password(password):
    password.strip()

    if len(password) < 8:
        return False, "Sua senha deve conter pelo menos 8 caracteres"
    if " " in password:
        return False, "Sua senha não pode conter espaços"
    return True, ""

def validate_name_or_email(info):
    if not info:
        return False, "Digite seu nome de usuário ou email"

    if re.match(EMAIL_PATTERN, info):
        user = User.query.filter_by(email=info).first()
    else:
        info = info.lower()
        user = User.query.filter_by(name=info).first()

    if not user:
        return False, "Nome de usuário ou email não registrados"

    return True, user

def validate_password(password, info):
    if not password:
        return False, "Digite uma senha"
    
    validation, result = validate_name_or_email(info)
    if not validation:
        return False, "Ocorreu um erro ao verificar a senha"

    if not check_password_hash(result.password_hash, password + result.password_token):
        return False, "Senha incorreta"
    
    return True, ""