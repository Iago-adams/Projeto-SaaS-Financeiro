from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Entrar')

class RegisterCompanyForm(FlaskForm):
    name = StringField('Nome da empresa', validators=[DataRequired()])
    cnpj = StringField('CNPJ', validators=[DataRequired()])
    btnSubmit = SubmitField ('Registrar empresa')

class RegisterSecretForm(FlaskForm):
    agencyId = StringField('Número da agência', validators=[DataRequired()])
    accountId = StringField('Número da Conta', validators=[DataRequired()])
    clientId = PasswordField('Cliente id', validators=[DataRequired()])
    clientSecret = PasswordField('Client Secret', validators=[DataRequired()])
    btnSubmit = SubmitField ('Cadastrar credenciais')

class RegisterCEOForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('password')])
    btnSubmit = SubmitField('Registrar CEO')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    btnSubmit = SubmitField('Solicitar')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nova senha', validators=[DataRequired()])
    password_confirm = PasswordField('Confirmar nova senha', validators=[DataRequired(), EqualTo('password')])
    btnSubmit = SubmitField('Redefinir')