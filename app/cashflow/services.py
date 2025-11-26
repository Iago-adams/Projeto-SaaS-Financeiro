#Pedir ao data fetcher os dados e em seguida pedir ao charts para gerar o grafico
from .data_fetcher import get_financial_JSON
from .analysis import generate_lineGraph_extract_html, normalize_JSON_transactions, calculate_kpis_from_dataframe
from .reports import generate_cashflow_PDF
from ..models import CompanyMembers, Role, Permissions, RolePermissions, User
from .tasks import send_reports_background

def generate_extract_graph(account_id, agency_id):
    #pega os dados da API de extrato bancario
    extract_API_data = get_financial_JSON(account_id, agency_id)
    
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

#função desgraçada maldita mal amada que nao funciona, DESGRAÇA
'''def send_cashflow_pdf(acount_id, company_name):
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
    return None'''
    
def send_cashflow_pdf(account_id, agency_id , company_name):
    # ... (sua parte de gerar o PDF continua igual) ...
    extract_API_data = get_financial_JSON(account_id, agency_id)
    normalized_df = normalize_JSON_transactions(extract_API_data)
    kpis = calculate_kpis_from_dataframe(normalized_df)
    pdf_bytes = generate_cashflow_PDF(company_name, kpis, normalized_df)
    
    recipient_emails = []

    print(f"\n--- INICIANDO DEBUG MANUAL PARA EMPRESA ID: {account_id} ---")
    
    # PASSO 1: Buscar membros sem JOIN
    # Força conversão para INT caso esteja vindo como String
    members = CompanyMembers.query.filter_by(company_id=int(account_id)).all()
    print(f"1. Membros encontrados na empresa: {len(members)}")

    for m in members:
        print(f"   > Analisando User ID: {m.user_id} | Role ID: {m.role_id}")
        
        # PASSO 2: Buscar o Usuário manualmente
        user = User.query.get(m.user_id)
        if not user:
            print("     [ERRO] Usuário não existe na tabela User.")
            continue
            
        # PASSO 3: Buscar o Role manualmente
        role = Role.query.get(m.role_id)
        if not role:
            print("     [ERRO] Role (Cargo) não existe.")
            continue
        print(f"     - Nome do Cargo: {role.name}")

        # PASSO 4: Buscar Permissões na "unha" (Sem confiar no relationship)
        # Vamos buscar direto na tabela de ligação
        role_perms = RolePermissions.query.filter_by(role_id=role.id).all()
        print(f"     - Qtd de Permissões encontradas para este cargo: {len(role_perms)}")
        
        tem_permissao = False
        for rp in role_perms:
            # PASSO 5: Ver qual é a permissão
            p = Permissions.query.get(rp.permission_id)
            print(f"       -> Permissão ID {p.id}: {p.codename}")
            if p.codename == 'cashflow':
                tem_permissao = True
        
        if tem_permissao:
            print(f"     [SUCESSO] O usuário {user.email} TEM A PERMISSÃO!")
            recipient_emails.append(user.email)
        else:
            print(f"     [FALHA] O usuário {user.email} NÃO tem permissão 'cashflow'.")

    print(f"--- FIM DO DEBUG. Destinatários finais: {recipient_emails} ---\n")

    # --- MODO DE EMERGÊNCIA (SALVA-VIDAS DA APRESENTAÇÃO) ---
    # Se a lista estiver vazia (erro de banco), manda para quem está logado.
    if not recipient_emails:
        print("!!! LISTA VAZIA - ATIVANDO MODO DE EMERGÊNCIA !!!")
        from flask_login import current_user
        if current_user.is_authenticated:
            print(f"Enviando para o usuário logado: {current_user.email}")
            recipient_emails.append(current_user.email)

    # Envia email (Task)
    if recipient_emails:
        send_reports_background(pdf_bytes, recipient_emails, company_name)
    
    return None