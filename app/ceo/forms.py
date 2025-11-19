from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets import ListWidget, CheckboxInput

class CheckBoxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class RoleForm(FlaskForm):
    name = StringField('Nome da função', validators=[DataRequired()])
    permissions = CheckBoxField('Permissões da função', coerce=int, choices=[], validators=[Length(min=1, message="Selecione ao menos um campo de permissão")])
    btnSubmit = SubmitField('Criar')
            


class MemberForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Função', choices=[], coerce=int, validators=[DataRequired()])
    btnSubmit = SubmitField('Cadastrar')


class EditMemberForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Função', choices=[], coerce=int, validators=[DataRequired()])
    permissions = CheckBoxField('Permissões da função', coerce=int, choices=[], validators=[Length(min=1, message="Selecione ao menos um campo de permissão")])
    btnSubmit = SubmitField('Salvar')