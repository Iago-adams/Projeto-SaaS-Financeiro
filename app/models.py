from .extensions import db
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from .services.hashing import hash_password, verify_password
import datetime
from .services.encryption import encrypt, decrypt
import json

class User(db.Model, UserMixin):    
    id = db.Column(db.Integer, primary_key=True)    
    username = db.Column(db.String(64), unique=True, nullable=False)    
    email = db.Column(db.String(120), unique=True, nullable=False)    
    password_hash = db.Column(db.String(255), nullable=False)       
    isSuperUser = db.Column(db.Boolean, nullable=False, default=False)

    membership = db.relationship('CompanyMembers', foreign_keys='CompanyMembers.user_id', back_populates='user', uselist=False, cascade="all, delete-orphan")

    #recebe a senha e hasheia ela
    def set_password(self, password):
        #Define o hash da senha
        self.password_hash = hash_password(password)
    
    #função para verificação de senha (login)
    def password_check(self, password): 
        #verifica a senha com o hash
        return verify_password(password, self.password_hash)
    
    #cria um token para a redefinição de senha
    def generate_token_password(self):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

        return serializer.dumps(self.email, salt=self.password_hash)
    
    @property
    def permissions(self):
        if not self.membership:
            return []
        
        perms = self.membership.role.permissions
        '''for perm in perms:
            print(perm.permission.codename)'''
        return [p.permission.codename for p in perms]
    
    def has_permission(self, codename):
        if self.permissions == []:
            return False
        
        elif codename in self.permissions:
            return True
    
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


    # Relações de volta para as tabelas principais
    user = db.relationship('User', back_populates='membership', uselist=False)
    company = db.relationship('Company', back_populates='members')
    role = db.relationship('Role', back_populates='members')


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    cnpj = db.Column(db.String(20), unique=True, nullable=False)


    # Relação: Uma empresa tem um conjunto de segredos (one-to-one).
    secrets = db.relationship('Secrets', back_populates='company', uselist=False, cascade="all, delete-orphan")
    # Relação: Uma empresa tem vários membros.
    members = db.relationship('CompanyMembers', back_populates='company', cascade="all, delete-orphan")
    # Relação: Uma empresa define várias funções (roles).
    roles = db.relationship('Role', back_populates='company', cascade="all, delete-orphan")
    # Relação: Uma empresa possui vários APIData (1-n)
    data = db.relationship('APIData', back_populates='company', cascade="all, delete-orphan")


class Secrets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(128), unique=True, nullable=False) #não precisa de criptografia
    agency_id = db.Column(db.String(128), unique=False, nullable=False)#não precisa de criptografia
    client_id = db.Column(db.String(256), unique=True, nullable=False) #encryptado
    client_secret = db.Column(db.String(256), nullable=False) #encryptado
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)


    # Relação: Segredos pertencem a uma única empresa.
    company = db.relationship('Company', back_populates='secrets')


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    # Relação: A função pertence a uma empresa.
    company = db.relationship('Company', back_populates='roles')
    # Relação: Vários membros da empresa podem ter esta função.
    members = db.relationship('CompanyMembers', back_populates='role')
    # Relação: Uma função tem várias permissões através da tabela RolePermissions.
    permissions = db.relationship('RolePermissions', foreign_keys='RolePermissions.role_id', back_populates='role', cascade="all, delete-orphan")

class RolePermissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=False)

    # Relações de volta para Role e Permission
    role = db.relationship('Role', foreign_keys=role_id, back_populates='permissions')
    permission = db.relationship('Permissions', foreign_keys=permission_id, back_populates='roles')

class Permissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    codename = db.Column(db.String(64), unique=True, nullable=False)

    # Relação: Uma permissão pode estar associada a várias funções através da tabela RolePermissions.
    roles = db.relationship('RolePermissions', foreign_keys='RolePermissions.permission_id', back_populates='permission')


class APIData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encrypt_data = db.Column(db.Text, nullable=False)
    last_update = db.Column(db.DateTime, default=datetime.datetime.now)
    expires = db.Column(db.DateTime, nullable=False) #last update+10 min
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    # Relação: Uma APIData pertence a uma única empresa
    company = db.relationship('Company', back_populates='data')

    def is_valid(self):
        return datetime.now() < self.expires
    
    def update_data(self, json):
        json_str = json.dumps(json)
        self.encrypt_data = encrypt(json_str)
        self.last_update = datetime.datetime.now()
    
    @property
    def data(self):
        decrypted_str = decrypt(self.encrypt_data)
        return json.loads(decrypted_str)