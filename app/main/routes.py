from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_user, logout_user, login_required


main_bp = Blueprint(
    'main', 
    __name__,  
    template_folder='templates'
    )

#Rota de login de usuário
@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def homepage():
    
    return render_template('homepage.html')
