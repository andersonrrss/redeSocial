# Configurações do aplicativo Flask
SECRET_KEY = 'a1b2c3'
TEMPLATES_AUTO_RELOAD = True
SESSION_PERMANENT = True
SESSION_TYPE = 'filesystem'

# Configurações do SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
