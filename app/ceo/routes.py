from flask import Blueprint, render_template
from models import User
from flask_login import current_user
from ..decorators import ceo_required

ceo_bp = Blueprint('ceo', __name__, url_prefix='/ceo', template_folder='./templates')


#rota básica do ceo, deve listar todos os membros
@ceo_bp.route('/')
@ceo_required
def ceo_page():
    members = User.query.filter_by(User.company.id==current_user.company.id)

    return render_template('ceo.html', members=members)

@ceo_bp.route('/adicionar/colaborador/')
@ceo_required
def add_member():
    pass

@ceo_bp.route('/editar/<int:id>/colaborador/')
@ceo_required
def edit_member(id):
    pass

@ceo_bp.route('/deletar/<int:id>/colaborador/')
@ceo_required
def delete_member(id):
    pass