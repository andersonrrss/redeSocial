from flask import Flask
from flask_migrate import Migrate
from flask_session import Session
from flask_socketio import SocketIO
from .models import db
from .helpers import inject_user

socketio = SocketIO(cors_allowed_origins="*")
migrate = Migrate()

def create_app():
    # Configurações da aplicação
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Iniciando o banco de dados
    db.init_app(app)
    migrate.init_app(app,db)
    # Sessão
    Session(app)

    # Inicializando o socketio
    socketio.init_app(app)

    # Importar as rotas depois da criação da aplicação
    from .views import register_blueprints
    register_blueprints(app)

    # Criar todas as tabelas
    with app.app_context():
        db.create_all()  # Cria todas as tabelas definidas nos modelos

    # Registro do context processor
    app.context_processor(inject_user)

    return app, socketio