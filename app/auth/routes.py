from flask import Blueprint, flash, redirect, render_template, url_for
from app.models import User
from .forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required
from app.extensions import db

auth_bp = Blueprint(
    'auth', 
    __name__,  
    template_folder='templates'
    )

#Rota de login de usuário
@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).scalar()

        if user:
            if user.password_check(form.password.data):
                login_user(user)
                flash(f'Bem vindo {user.username}', 'success')
                return redirect(url_for('main.homepage'))
        else:
            flash('Credenciais incorretas', 'danger')
    
    return render_template('login.html', form=form)


@auth_bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))


@auth_bp.route('/register/', methods=['GET', 'POST'])
def registerCEO():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            isSuperUser=False
        )
        user.set_password(form.password.data)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Usuário registrado com sucesso', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(e)
            flash('Erro ao registrar usuário', 'danger')
            
    return render_template('register.html', form=form)