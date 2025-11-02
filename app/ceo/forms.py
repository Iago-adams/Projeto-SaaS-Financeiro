from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email

class RoleForm(FlaskForm):
    name = StringField('Nome da função', validators=[DataRequired()])
    permissions = SelectMultipleField('Permissões da função', choices=[], coerce=int, validators=[DataRequired()])
    btnSubmit = SubmitField('Criar')

class MemberForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Função', choices=[], coerce=int, validators=[DataRequired()])
    btnSubmit = SubmitField('Cadastrar')