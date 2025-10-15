#init padrão onde esta centraluizada todas as inicializações
from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager
#só pra explicar o ponto ajuda o flask a saber que o arquivos estão nesta mesma pasta o que ajuda na velocidade
#explicação tecnica pro ponto é que ele manda o flask procurar no mesmo pacote basicamente

def create_app(config_class=Config):

    #Inicialização do Flask padrão
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    #Inicialização de todas as extenções do extension.py
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    #Registro das blueprints
    #
    #inicialização das blueprints devem ficar aqui, não fiz porque eu ainda não exatamente como funciona (é a proxima coisa que eu vou estudar)
    #
    
    return app