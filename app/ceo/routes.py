from flask import Blueprint, render_template, flash, redirect, url_for
from app import db
from app.models import User, Role, Permissions, CompanyMembers
from flask_login import current_user
from ..decorators import ceo_required
from .forms import RoleForm, MemberForm
from auth.utils import send_first_password, generate_password

ceo_bp = Blueprint('ceo', __name__, template_folder='./templates')

#rota básica do ceo, deve listar todos os membros
@ceo_bp.route('/')
def ceo_page():
    members = User.query.filter_by(User.company.id==current_user.company.id)

    return render_template('ceo.html', members=members)

@ceo_bp.route('/adicionar/colaborador/')
def add_member():
    form = MemberForm()

    form.role.choices[Role.query.all()]

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(generate_password())

        member = CompanyMembers(
            company_id=current_user.membership.company_id,
            role_id=form.role.data
        )

        db.session.add(user)
        db.session.add(member)
        db.session.commit()

        flash(f'{form.username.data} foi adicionado ao sistema', 'success')

        return redirect(url_for('ceo.ceo_page'))
    
    return render_template('add_member.html', form=form)

@ceo_bp.route('/editar/<int:id>/colaborador/')
def edit_member(id):
    pass

@ceo_bp.route('/deletar/<int:id>/colaborador/')
def delete_member(id):
    pass

@ceo_bp.route('/adicionar/papel/')
def add_role():
    form = RoleForm()

    form.permissions.choices[Permissions.query.all()]

    if form.validate_on_submit():
        role = Role(
            name=form.name.data,
            company_id=current_user.membership.company_id
        )

        for perm in form.permissions.data:
            role.permissions = perm
        
        db.session.add(role)
        db.session.commit()

        flash(f'Função {role.name} foi criada', 'success')

        return redirect(url_for('ceo.ceo_page'))

    return render_template('add_role.html', form=form)