#este aquivo é responsavel pelas extensões do flask(migrate, sqalchemy, entra ouitra que agente for usar)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()