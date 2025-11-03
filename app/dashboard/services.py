#Pedir ao data fetcher os dados e em seguida pedir ao charts para gerar o grafico
from .data_fetcher import get_financial_JSON
from .charts import generate_lineGraph_extract

def generate_extract_graph():
    #pega os dados da API de extrato bancario
    extract_API_data = get_financial_JSON()
    
    #gera o JSON que vai ser lido pelo html com o grafico em linha
    lineGraph_extract_html = generate_lineGraph_extract(extract_API_data)
    return lineGraph_extract_html