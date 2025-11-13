#init padrão onde esta centraluizada todas as inicializações
from flask import Flask
from . import config
from .extensions import db, migrate, login_manager, mail
from .models import User, Permissions
#só pra explicar o ponto ajuda o flask a saber que o arquivos estão nesta mesma pasta o que ajuda na velocidade
#explicação tecnica pro ponto é que ele manda o flask procurar no mesmo pacote basicamente

def create_permissions():
    perms = {'CEO':'Acesso as configuração da empresa',
             'cashflow':'Acesso ao fluxo de caixa', } #caso necessário só aumentar a key e o codename o value o name

    for perm in perms: #ele vai entrar e pegar as keys do dict e vai adicionar no db
        verify = Permissions.query.filter_by(codename=perm).first()

        if verify is None:
            permission = Permissions(
                name=perms[perm],
                codename=perm
            )

            db.session.add(permission)
            db.session.commit()
            print(f'{perm} foi criada')
        else:
            print(f'{perm} já está criada')
        

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
    from .cashflow.routes import cashflow_bp
    from .ceo.routes import ceo_bp
    from .errors.errors import errors_bp

    #Registro das blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(cashflow_bp, url_prefix='/cashflow')
    app.register_blueprint(ceo_bp, url_prefix='/ceo')
    app.register_blueprint(errors_bp, url_prefix='/error')
        
    
    return app