from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from app import db
from app.models import User, Role, Permissions, CompanyMembers, RolePermissions
from flask_login import current_user
from .forms import RoleForm, MemberForm, EditMemberForm
from ..auth.utils import send_first_password, generate_password
from ..decorators import permission_required
from sqlalchemy import or_

ceo_bp = Blueprint('ceo', __name__, template_folder='./templates')

#rota básica do ceo, deve listar todos os membros
@ceo_bp.route('/', methods=['GET', 'POST'])
@permission_required
def ceo_page():

    pesquisa = request.args.get('pesquisa', '')

    query = CompanyMembers.query.join(User).filter(
        CompanyMembers.company_id == current_user.membership.company_id
    )
    if pesquisa and pesquisa != '':
        query = query.filter(
            or_(
                User.username.ilike(f'%{pesquisa}%'),
                User.email.ilike(f'%{pesquisa}%'),
            )
        )

    members = query.all()

    return render_template('ceo.html', members=members)

@ceo_bp.route('/adicionar/funcionario/', methods=['GET', 'POST'])
def add_member():
    form = MemberForm()

    roles = Role.query.all()

    form.role.choices = [(r.id, r.name) for r in roles]

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
        )

        password = generate_password()
        user.set_password(password)

        member = CompanyMembers(
            company_id=current_user.membership.company_id,
            role_id=form.role.data
        )

        user.membership = member

        db.session.add(user)
        db.session.add(member)
        db.session.commit()

        send_first_password(user, password)

        flash(f'{form.username.data} foi adicionado ao sistema', 'success')

        return redirect(url_for('ceo.ceo_page'))
    
    return render_template('add_member.html', form=form)

@ceo_bp.route('/editar/<int:id>/funcionario/', methods=['GET', 'POST'])
def edit_member(id):
    user = User.query.get_or_404(id)
    form = EditMemberForm()

    roles = Role.query.filter(Role.company_id==current_user.membership.company_id).all()
    permissions = []
    for role in roles:
        for perms in role.permissions:
            if perms.permission not in permissions:
                permissions.append(perms.permission)

    form.role.choices = [(r.id, r.name) for r in roles]
    form.permissions.choices = [(p.id, p.name) for p in permissions]

    form.username.default = user.username

    if form.validate_on_submit():
        print("validou o form")
        user.username = form.username.data
        user.email = form.email.data
        user.membership.role_id = form.role.data
        user.membership.role.permissions_id = form.permissions.data
        db.session.commit()
        flash(f'Informações de {user.username} foram atualizadas', 'success')
        return redirect(url_for('ceo.ceo_page'))
    
    return render_template('edit_member.html', form=form, user=user)

@ceo_bp.route('/deletar/<int:id>/funcionario/', methods=['POST'])
def delete_member(id):
    user = User.query.get(id)

    if user:
        nome = user.username
        db.session.delete(user)
        db.session.commit()

        flash(f'{nome} foi removido do sistema', 'warning')

        return redirect(url_for('ceo.ceo_page'))
    
    return abort(404)

@ceo_bp.route('/adicionar/funcao/', methods=['GET', 'POST'])
def add_role():
    form = RoleForm()

    form.permissions.choices=[(p.id, p.name) for p in Permissions.query.all()]

    if form.validate_on_submit():
        role = Role(
            name=form.name.data,
            company_id=current_user.membership.company_id
        )
        db.session.add(role)
        db.session.commit()

        perms = Permissions.query.filter(Permissions.id.in_(form.permissions.data)).all()
        print(perms)

        role_perms = []
        
        for perm in perms:
            role_perm = RolePermissions(
                role_id=role.id,
                permission_id = perm.id
            )

            role_perms.append(role_perm)
    
        role.permissions = role_perms
        
        db.session.commit()

        flash(f'Função {role.name} foi criada', 'success')

        return redirect(url_for('ceo.ceo_page'))

    return render_template('add_role.html', form=form)

