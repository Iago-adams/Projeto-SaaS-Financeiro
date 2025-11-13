#Pedir ao data fetcher os dados e em seguida pedir ao charts para gerar o grafico
from .data_fetcher import get_financial_JSON
from .analysis import generate_lineGraph_extract, normalize_JSON_transactions, calculate_kpis_from_dataframe

def generate_extract_graph():
    #pega os dados da API de extrato bancario
    extract_API_data = get_financial_JSON()
    
    #Normaliza os dados para enviar o gerenerate line graph
    normalized_JSON = normalize_JSON_transactions(extract_API_data)
    
    #gera o JSON que vai ser lido pelo html com o grafico em linha
    lineGraph_extract_html = generate_lineGraph_extract(normalized_JSON)
    return lineGraph_extract_html

def get_cashflow_kpis_json():
    #função que vai servir para retornar o kpis para um endpoint que vai ser acessado pelo RF, para testar o sistema
    extract_API_data = get_financial_JSON()
    normalized_df = normalize_JSON_transactions(extract_API_data)
    
    # Para aqui e retorna os dados calculados
    kpis = calculate_kpis_from_dataframe(normalized_df)
    
    return kpis