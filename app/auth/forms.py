from flask_wtf import FlaskForm
<<<<<<< HEAD
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Entrar')

class RegisterCompanyForm(FlaskForm):
    name = StringField('Nome da empresa', validators=[DataRequired()])
    cnpj = IntegerField('CNPJ', validators=[DataRequired()])
    btnSubmit = SubmitField ('Registrar empresa')

class RegisterSecretForm(FlaskForm):
    clientId = StringField('Cliente id', validators=[DataRequired()])
    clientSecret = StringField('Client Secret', validators=[DataRequired()])
    btnSubmit = SubmitField ('Cadastrar credenciais')

class RegisterCEOForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Registrar CEO')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    btnSubmit = SubmitField('Solicitar')
=======
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
>>>>>>> e7729cb66c56b9a29352122f71d6d80053002669

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nova senha', validators=[DataRequired()])
    password_confirm = PasswordField('Confirmar nova senha', validators=[DataRequired(), EqualTo(password)])
    btnSubmit = SubmitField('Redefinir')