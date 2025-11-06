from flask import Blueprint, render_template, jsonify
#from ..decorators import permission_required
from .services import generate_extract_graph, get_dashboard_kpis_json

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

#Rota para o teste com o FK
@dashboard_bp.route('/kpis', methods=['GET'])
def dashboard_kpis():
    kpis = get_dashboard_kpis_json() # Chama o Serviço 2
    return jsonify(kpis), 200