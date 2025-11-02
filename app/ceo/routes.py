from flask import Blueprint, render_template
from app.models import User
from flask_login import current_user
from ..decorators import ceo_required

ceo_bp = Blueprint('ceo', __name__, template_folder='./templates')

#rota básica do ceo, deve listar todos os membros
@ceo_bp.route('/')
def ceo_page():
    members = User.query.filter_by(User.company.id==current_user.company.id)

    return render_template('ceo.html', members=members)

@ceo_bp.route('/adicionar/colaborador/')
def add_member():
    pass

@ceo_bp.route('/editar/<int:id>/colaborador/')
def edit_member(id):
    pass

@ceo_bp.route('/deletar/<int:id>/colaborador/')
def delete_member(id):
    pass