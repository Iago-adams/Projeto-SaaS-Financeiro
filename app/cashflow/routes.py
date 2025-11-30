from flask import Blueprint, render_template, jsonify, redirect, url_for, abort
#from ..decorators import permission_required
from .services import generate_extract_graph, get_cashflow_kpis_json, send_cashflow_pdf
from flask_login import login_required, current_user

cashflow_bp = Blueprint(
    'cashflow', 
    __name__,  
    template_folder='./templates'
    )

#Rota de login de exibir o grafico
@cashflow_bp.route('/', methods=['GET', 'POST'])
def cashflow():
    tenantAgency_id = current_user.membership.company.secrets.agency_id
    tenantAccount_id = current_user.membership.company.secrets.account_id
    
    graph_extract_line_html = generate_extract_graph(account_id = tenantAccount_id, agency_id = tenantAgency_id)
    return render_template('cashflow.html', graph_extract_line=graph_extract_line_html)

#rota para enviar relatorio
@cashflow_bp.route('/send-report')
def send_report():
    tenantAgency_id = current_user.membership.company.secrets.agency_id
    tenantAccount_id = current_user.membership.company.secrets.account_id
    tenant_name = current_user.membership.company.name
    
    send_cashflow_pdf(account_id=tenantAgency_id, agency_id=tenantAccount_id, company_name=tenant_name)#retorna a função para enviar o pdf com extrato bancário do service
    return redirect(url_for('cashflow.cashflow'))

#Rota para o teste com o FK
@cashflow_bp.route('/kpis', methods=['GET'])
def cashflow_kpis():
    kpis = get_cashflow_kpis_json() # Chama o Serviço 2
    return jsonify(kpis), 200