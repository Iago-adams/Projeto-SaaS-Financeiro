from flask import Blueprint, flash, redirect, render_template, url_for, session
from app.models import User, Company, Secrets, Role
from .forms import LoginForm, RegisterCompanyForm, RegisterSecretForm, RegisterCEOForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from .utils import create_ceo

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='./templates')

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


@auth_bp.route('/register/company/', methods=['GET', 'POST'])
def register_company():
    form = RegisterCompanyForm()

    if form.validate_on_submit():

        #armazena os dados do forms na sessão e armazena como FormCompany
        session['FormCompany'] = {
            'name': form.name.data,
            'cnpj': form.cnpj.data
        }
        
        return redirect(url_for('register_secrets'))

    return render_template('register_company.html', form=form)
    
@auth_bp.route('/register/secrets/', methods=['GET', 'POST'])
def register_secrets():
    form = RegisterSecretForm()

    if form.validate_on_submit():

        #armazena os dados do forms na sessão e armazena como FormsSecrets
        session['FormSecrets'] = {
            'clientId': form.clientId.data,
            'clientSecret': form.clientSecret.data
        }

        return redirect(url_for('register_ceo'))
    
    return render_template('register_secrets.html', form=form)

@auth_bp.route('/register/ceo/', methods=['GET', 'POST'])
def register_ceo():
    
    form = RegisterCEOForm()

    if form.validate_on_submit():

        #puxa os dados da sessão
        FormCompany = session.get('FormCompany', {})

        #passa diretamente pro company que sera commitado no db
        company = Company(**FormCompany)
        db.session.add(company)
        db.session.commit()

        #puxa os dados da sessão
        FormSecrets = session.get('FormSecrets', {})

        #passa diretamente pro secrets que sera commitado no db
        secrets = Secrets(company_id=company.id, **FormSecrets)
        db.session.add(secrets)
        db.session.commit()

        ceo = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(ceo)
        db.session.commit()

        #puxa a função para já criar a role ceo na empresa
        create_ceo(company.id, ceo.id)

        return redirect(url_for('main.index'))
    
    return render_template('register_ceo.html', form=form)

@auth_bp.route('/request/reset/password/', methods=['GET', 'POST'])
def request_password():

    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    
    else:
        form = RequestResetForm()

        if form.validate_on_submit():
            flash('Confira seu email para redefinir sua senha', 'warning')

            user = User.query.filter_by(email=form.email.data).scalar()

            return redirect(url_for('request_password'))

    return render_template('request_password.html', form=form)

@auth_bp.route('/reset/password/', methods=['GET', 'POST'])
def reset_password(token, id):
    user = User.verify_token(token, id)

    if user:
        form = ResetPasswordForm()

        if form.validate_on_submit():
            user.set_password(form.password.data)

            return redirect(url_for('login'))
    
    return render_template('reset_password.html', form=form)

