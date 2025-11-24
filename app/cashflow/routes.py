from flask import Blueprint, render_template, jsonify, redirect, url_for
#from ..decorators import permission_required
from .services import generate_extract_graph, get_cashflow_kpis_json, send_cashflow_pdf
from flask_login import login_required, current_user

cashflow_bp = Blueprint(
    'cashflow', 
    __name__,  
    template_folder='./templates'
    )

#Rota de login de usuário
@cashflow_bp.route('/', methods=['GET', 'POST'])
def cashflow():
    tenant_id = current_user.membership.company_id
    
    graph_extract_line_html = generate_extract_graph(acount_id = tenant_id)
    return render_template('cashflow.html', graph_extract_line=graph_extract_line_html)

@cashflow_bp.route('/send-report')
def send_report():
    tenant_id = current_user.membership.company_id
    tenant_name = current_user.membership.company.name
    
    send_cashflow_pdf(acount_id = tenant_id, company_name = tenant_name)#retorna a função para enviar o pdf com extrato bancário do service
    return redirect(url_for('cashflow.cashflow'))

#Rota para o teste com o FK
@cashflow_bp.route('/kpis', methods=['GET'])
def cashflow_kpis():
    kpis = get_cashflow_kpis_json() # Chama o Serviço 2
    return jsonify(kpis), 200