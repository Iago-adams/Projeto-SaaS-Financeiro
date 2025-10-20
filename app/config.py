#Centralizar todas as variáveis de configuração da aplicação(como chaves secretas, uri do banco de dados, etc)

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
    
#Configuração para o banco de dados
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False

#Configurações Flask_Mail
MAIL_SERVER= os.environ.get('MAIL_SERVER')
MAIL_PORT = os.environ.get('MAIL_PORT')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
    
#recebendo a chave de criptografia usada pela biblioteca cryptography
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
   
#esse if verifica que a chave de cryptografia foi definida no .env para garantir a segurança e funcionamento do sistema
if os.environ.get('FLASK_ENV') == 'production' and not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY não definida nas variáveis de ambiente.")