#Centralizar todas as variáveis de configuração da aplicação(como chaves secretas, uri do banco de dados, etc)

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
    
#Configuração para o banco de dados
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
    
#recebendo a chave de criptografia usada pela biblioteca cryptography
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
   
#esse if verifica que a chave de cryptografia foi definida no .env para garantir a segurança e funcionamento do sistema
if os.environ.get('FLASK_ENV') == 'production' and not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY não definida nas variáveis de ambiente.")