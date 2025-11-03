#Centralizar todas as variáveis de configuração da aplicação(como chaves secretas, uri do banco de dados, etc)

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

# Configuração do Banco de Dados PostgreSQL
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# URI de Conexão do SQLAlchemy
# Formato: postgresql://[user]:[password]@[host]:[port]/[dbname]
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
    
# Opcional, mas recomendado: desativa o rastreamento de modificações
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