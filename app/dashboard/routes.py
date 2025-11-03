from flask import Blueprint, flash, redirect, render_template, url_for
#from ..decorators import ceo_required
from .services import generate_extract_graph

dashboard_bp = Blueprint(
    'dashboard', 
    __name__,  
    template_folder='./templates'
    )

#Rota de login de usuário
@dashboard_bp.route('/', methods=['GET', 'POST'])
def dashboard():
    graph_extract_line_html = generate_extract_graph()
    return render_template('dashboard.html', graph_extract_line=graph_extract_line_html)