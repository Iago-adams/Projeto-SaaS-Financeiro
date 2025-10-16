#init padrão onde esta centraluizada todas as inicializações
from flask import Flask
from . import config
from .extensions import db, migrate, login_manager, mail
from .models import User
#só pra explicar o ponto ajuda o flask a saber que o arquivos estão nesta mesma pasta o que ajuda na velocidade
#explicação tecnica pro ponto é que ele manda o flask procurar no mesmo pacote basicamente

def create_app(config_class=config):

    #Inicialização do Flask padrão
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    #Inicialização de todas as extenções do extension.py
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    

    #Configuração do login manager
    login_manager.login_view = 'auth.login' # Rota para usuarios não autenticados
    login_manager.login_message_category = 'info' # Categoria da mensagem flash

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    #Import das blueprints
    from .auth.routes import auth_bp
    from .main.routes import main_bp

    #Registro das blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp, url_prefix='/')
        
    
    return app