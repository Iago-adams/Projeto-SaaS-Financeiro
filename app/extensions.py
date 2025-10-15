#este aquivo é responsavel pelas extensões do flask(migrate, sqalchemy, entra ouitra que agente for usar)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()