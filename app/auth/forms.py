from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Entrar')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nova senha', validators=[DataRequired()])
    password_confirm = PasswordField('Confirmar nova senha', validators=[DataRequired(), EqualTo(password)])
    btnSubmit = SubmitField('Redefinir')