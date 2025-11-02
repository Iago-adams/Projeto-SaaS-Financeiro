from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email

class RoleForm(FlaskForm):
    name = StringField('Nome da função', validators=[DataRequired()])

class MemberForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Função', choices=[], coerce=int)