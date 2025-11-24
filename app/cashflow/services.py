#Pedir ao data fetcher os dados e em seguida pedir ao charts para gerar o grafico
from .data_fetcher import get_financial_JSON
from .analysis import generate_lineGraph_extract_html, normalize_JSON_transactions, calculate_kpis_from_dataframe
from .reports import generate_cashflow_PDF
from ..models import CompanyMembers, Role, Permissions, RolePermissions, User
from .tasks import send_reports_background
from flask import abort

def generate_extract_graph(acount_id):
    #pega os dados da API de extrato bancario
    extract_API_data = get_financial_JSON(acount_id)
    
    #Normaliza os dados para enviar o gerenerate line graph
    normalized_JSON = normalize_JSON_transactions(extract_API_data)
    
    #gera o JSON que vai ser lido pelo html com o grafico em linha
    lineGraph_extract_html = generate_lineGraph_extract_html(normalized_JSON)
    return lineGraph_extract_html

def get_cashflow_kpis_json():
    #função que vai servir para retornar o kpis para um endpoint que vai ser acessado pelo RF, para testar o sistema
    extract_API_data = get_financial_JSON()
    normalized_df = normalize_JSON_transactions(extract_API_data)
    
    # Para aqui e retorna os dados calculados
    kpis = calculate_kpis_from_dataframe(normalized_df)
    
    return kpis

def send_cashflow_pdf(acount_id, company_name):
    extract_API_data = get_financial_JSON(acount_id)
    normalized_JSON = normalize_JSON_transactions(extract_API_data)
    kpis = calculate_kpis_from_dataframe(normalized_JSON)
    
    pdf = generate_cashflow_PDF(company_name, kpis, normalized_JSON)
    
    emailsList = []
    #busca no banco de dados todos os funcionarios com role cashflow, e chamar a task para gerar e enviar o pdf em segundo plano
    try:
        query_result = CompanyMembers.query \
            .join(User) \
            .join(Role) \
            .join(RolePermissions) \
            .join(Permissions) \
            .filter(
                CompanyMembers.company_id == acount_id,  # Filtra pela empresa
                Permissions.codename == 'cashflow'       # Filtra pela permissão exata
            ) \
            .with_entities(User.email) \
            .all()
            
        recipient_emails = [row[0] for row in query_result]    
    except Exception as e:
        print(f"Erro ao buscar membros: {e}")
        return abort(500)
    
    #passar pdf, ids dos funcionarios
    send_reports_background(pdf, emailsList, company_name)
    return None