from flask import Blueprint, flash, redirect, render_template, url_for, session
from app.models import User, Company, Secrets, Role
from .forms import LoginForm, RegisterCompanyForm, RegisterSecretForm, RegisterCEOForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from .utils import create_ceo, validate_password_policy

auth_bp = Blueprint(
    'auth', 
    __name__, 
    url_prefix='/auth', 
    template_folder='./templates'
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
        
        return redirect(url_for('auth.register_secrets'))

    return render_template('register_company.html', form=form)
    
@auth_bp.route('/register/secrets/', methods=['GET', 'POST'])
def register_secrets():
    form = RegisterSecretForm()

    if form.validate_on_submit():

        #armazena os dados do forms na sessão e armazena como FormsSecrets
        session['FormSecrets'] = {
            'acount_id': form.acountId.data,
            'client_id': form.clientId.data,
            'client_secret': form.clientSecret.data
        }

        return redirect(url_for('auth.register_ceo'))
    
    return render_template('register_secrets.html', form=form)

@auth_bp.route('/register/ceo/', methods=['GET', 'POST'])
def register_ceo():
    
    form = RegisterCEOForm()

    if form.validate_on_submit():

        #puxa os dados da sessão
        FormCompany = session.get('FormCompany', {})

        #passa diretamente pro company que sera commitado no db
        company = Company(**FormCompany)
        #verifica se a empresa ja esta cadastrada
        verify_company = Company.query.filter_by(cnpj=company.cnpj).first()
        if verify_company:
            flash('CNPJ já cadastrado no sistema.', 'danger')
            return redirect(url_for('auth.register_company'))
        #cadastra a empresa

        #puxa os dados da sessão
        FormSecrets = session.get('FormSecrets', {})

        #passa diretamente pro secrets que sera commitado no db
        secrets = Secrets(company_id=company.id, **FormSecrets)
        #verifica se os secrets ja estao cadastrados
        verify_account_id = Secrets.query.filter_by(acount_id=secrets.acount_id).first()
        verify_client_id = Secrets.query.filter_by(client_id=secrets.client_id).first()
        if verify_account_id:
            flash('Ocorreu um erro inesperado.', 'danger')
            return redirect(url_for('auth.register_company'))
        if verify_client_id:
            flash('Ocorreu um erro inesperado.', 'danger')
            return render_template('register_ceo.html', form=form)
        #adiciona o secrets ao db
        
        #Verifica se o username e email já estão cadastrados
        verify_username = User.query.filter_by(username=form.username.data).first()
        if verify_username:
            flash('Nome já cadastrado no sistema.', 'danger')
            return redirect(url_for('auth.register_ceo'))
        verify_email = User.query.filter_by(email=form.email.data).first()
        if verify_email:
            flash('Nome já cadastrado no sistema.', 'danger')
            return redirect(url_for('auth.register_ceo'))
        
        #Cria o usuário CEO
        ceo = User(
            username=form.username.data,
            email=form.email.data,
        )

        #Checando segurança da senha
        password=form.password.data
        is_valid, error_message = validate_password_policy(password)
        if not is_valid:
            flash(error_message, 'danger')
            return redirect(url_for('auth.register_ceo'))

        ceo.set_password(form.password.data)
        db.session.add(ceo)
        db.session.add(company)
        db.session.add(secrets)
        db.session.commit()

        #puxa a função para já criar a role ceo na empresa
        create_ceo(company.id, ceo.id)

        login_user(ceo)

        return redirect(url_for('main.homepage'))
    
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

            user.generate_token_password()

            return redirect(url_for('auth.request_password'))

    return render_template('request_password.html', form=form)

@auth_bp.route('/reset/password/<id>/<token>/', methods=['GET', 'POST'])
def reset_password(token, id):
    user = User.verify_token(token, id)

    if not user:
        flash('Token expirado', 'danger')
        return redirect(url_for('auth.login'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        print(form.password.data)
        user.set_password(form.password.data)

        return redirect(url_for('auth.login'))
    
    return render_template('reset_password.html', form=form)
