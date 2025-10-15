from .extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):    
    id = db.Column(db.Integer, primary_key=True)    
    username = db.Column(db.String(64), unique=True, nullable=False)    
    email = db.Column(db.String(120), unique=True, nullable=False)    
    password = db.Column(db.String(128), nullable=False)       
    isSuperUser = db.Column(db.Boolean, nullable=False)

class CompanyMembers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

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

