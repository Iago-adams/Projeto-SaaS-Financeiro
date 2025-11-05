from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
    

class RoleForm(FlaskForm):
    name = StringField('Nome da função', validators=[DataRequired()])
    permissions = MultiCheckboxField('Permissões da função', coerce=int, validators=[DataRequired()])
    btnSubmit = SubmitField('Criar')


class MemberForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Função', choices=[], coerce=int, validators=[DataRequired()])
    btnSubmit = SubmitField('Cadastrar')