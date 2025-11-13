from flask import Blueprint, render_template, jsonify
#from ..decorators import permission_required
from .services import generate_extract_graph, get_cashflow_kpis_json

cashflow_bp = Blueprint(
    'cashflow', 
    __name__,  
    template_folder='./templates'
    )

#Rota de login de usuário
@cashflow_bp.route('/', methods=['GET', 'POST'])
def cashflow():
    graph_extract_line_html = generate_extract_graph()
    return render_template('cashflow.html', graph_extract_line=graph_extract_line_html)

#Rota para o teste com o FK
@cashflow_bp.route('/kpis', methods=['GET'])
def cashflow_kpis():
    kpis = get_cashflow_kpis_json() # Chama o Serviço 2
    return jsonify(kpis), 200