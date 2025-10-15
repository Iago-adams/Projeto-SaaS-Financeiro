from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField

from app import db
from models import User

class LoginForm(FlaskForm):
    username = StringField('Nome de usuário')