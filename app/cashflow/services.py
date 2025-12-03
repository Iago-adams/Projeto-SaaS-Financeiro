from flask import abort
from flask_login import current_user
from .data_fetcher import get_financial_JSON
from .analysis import generate_lineGraph_extract_html, normalize_JSON_transactions, calculate_kpis_from_dataframe
from .reports import generate_cashflow_PDF
from ..models import CompanyMembers, Role, Permissions, RolePermissions, User
from .tasks import send_reports_background

def generate_extract_graph(account_id, agency_id):
    """
    Gera o HTML do gráfico.
    """
    print(f"--- SERVICE: Buscando extrato. Conta: {account_id} | Agência: {agency_id} ---")
    
    try:
        # 1. Busca dados na API (ou Mock se falhar)
        extract_API_data = get_financial_JSON(account_id, agency_id)
        
        if not extract_API_data:
            print("--- SERVICE: Nenhum dado financeiro encontrado. ---")
            return None

        # 2. Normaliza os dados
        normalized_JSON = normalize_JSON_transactions(extract_API_data)
        
        if normalized_JSON.empty:
            print("--- SERVICE: Dados normalizados estão vazios. ---")
            return None

        # 3. Gera o HTML do gráfico
        lineGraph_extract_html = generate_lineGraph_extract_html(normalized_JSON)
        return lineGraph_extract_html

    except Exception as e:
        print(f"--- SERVICE ERROR: Falha ao gerar gráfico: {e} ---")
        return None

def get_cashflow_kpis_json():
    """
    Retorna os KPIs em JSON.
    CORREÇÃO: Agora busca os IDs do current_user antes de chamar a API.
    """
    try:
        if not current_user.is_authenticated:
            return {}

        # Pega os dados da empresa do usuário logado
        secrets = current_user.membership.company.secrets
        account_id = secrets.account_id
        agency_id = secrets.agency_id

        # Passa os IDs corretamente para a função
        extract_API_data = get_financial_JSON(account_id, agency_id) 
        
        if not extract_API_data:
            return {}

        normalized_df = normalize_JSON_transactions(extract_API_data)
        kpis = calculate_kpis_from_dataframe(normalized_df)
        return kpis

    except Exception as e:
        print(f"--- SERVICE ERROR: Falha ao calcular KPIs: {e} ---")
        return {}

def send_cashflow_pdf(account_id, agency_id, company_name):
    """
    Gera e envia o PDF por e-mail.
    """
    try:
        print("--- SERVICE: Iniciando geração de PDF ---")
        
        # 1. Busca dados
        extract_API_data = get_financial_JSON(account_id, agency_id)
        if not extract_API_data:
            print("--- SERVICE: Sem dados para gerar PDF. ---")
            return None
            
        normalized_df = normalize_JSON_transactions(extract_API_data)
        # Calcula KPIs (Saldo Atual) para exibir no PDF
        kpis = calculate_kpis_from_dataframe(normalized_df)
        
        # 2. Gera o PDF (bytes)
        # O novo PDF usa o dataframe para calcular Saldo Inicial/Final internamente
        pdf_bytes = generate_cashflow_PDF(company_name, kpis, normalized_df)
        
        # 3. Identifica destinatários
        recipient_emails = []
        
        try:
            members = CompanyMembers.query.filter_by(company_id=int(account_id)).all()
            for m in members:
                role_perms = RolePermissions.query.filter_by(role_id=m.role_id).all()
                for rp in role_perms:
                    perm = Permissions.query.get(rp.permission_id)
                    if perm and perm.codename == 'cashflow':
                        user = User.query.get(m.user_id)
                        if user:
                            recipient_emails.append(user.email)
                        break 
        except Exception as db_err:
            print(f"--- ERRO DB BUSCA USUARIOS: {db_err}")

        # Fallback de segurança
        if not recipient_emails:
            print("--- AVISO: Nenhum e-mail encontrado. Enviando para usuário logado. ---")
            if current_user.is_authenticated:
                recipient_emails.append(current_user.email)

        # 4. Envia task
        if recipient_emails:
            send_reports_background(pdf_bytes, recipient_emails, company_name)
            print(f"--- SERVICE: PDF enviado para {len(recipient_emails)} destinatários. ---")
        
        return None

    except Exception as e:
        print(f"--- SERVICE ERROR: Falha no envio do PDF: {e} ---")
        return None