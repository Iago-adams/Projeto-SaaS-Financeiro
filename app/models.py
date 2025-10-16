from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

class User(db.Model, UserMixin):    
    id = db.Column(db.Integer, primary_key=True)    
    username = db.Column(db.String(64), unique=True, nullable=False)    
    email = db.Column(db.String(120), unique=True, nullable=False)    
    password_hash = db.Column(db.String(128), nullable=False)       
    isSuperUser = db.Column(db.Boolean, nullable=False)


    company = db.relationship('CompanyMembres', foreign_keys='User.id', back_populates='members')

    #recebe a senha e hasheia ela
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    #função para verificação de senha (login)
    def password_check(self, password):
        return check_password_hash(self.password_hash, password)
    
    #cria um token para a redefinição de senha
    def generate_token_password(self):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

        return serializer.dumps(self.email, salt=self.password_hash)
    
    #Método que verifica se o token é válido
    @staticmethod
    def verify_token(token, user_id):
        user = User.query.get(user_id)

        if user:

            serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            try:
                token_user = serializer.loads(token, max_age=900, salt=user.password_hash)
            except:
                return None
            
            if token_user == user.email:
                return user
            
        else:
            return None

class CompanyMembers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    #relação com user para puxar o membro (CompanyMembers)
    members = db.relationship('User', foreign_keys='User.id', back_populates='company', lazy=True)
    role = db.relationship('Role')

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    cnpj = db.Column(db.String(20), unique=True, nullable=False)

class Secrets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(128), unique=True, nullable=False)
    client_secret = db.Column(db.String(256), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

class RolePermissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), nullable=False)

class Permissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    codename = db.Column(db.String(64), unique=True, nullable=False)

#precisa criar uma função before request para criar o banco de dados quando formos dar o deploy
#encriptar ou hashear o client_id e client_secret