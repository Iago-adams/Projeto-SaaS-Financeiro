#Requerir os dados da API
from ..services.extract_api import get_token, get_extract_data

def _get_decrypted_client_keys(acount_id):
    return None

def get_financial_JSON():#Para a aplicação prática precisa passar o acount_id
    #pegar a client id e a client secret descriptografadas
    #client_keys = _get_decrypted_client_keys(acount_id)
    
    #Insira as credenciais do usuario aqui, futuramente aqui estara a função de descriptografar e puxar do banco de dados, no momento só estão Strings quaisquer para teste com a API mock
    client_id = 'clientIDtest'
    client_secret = 'clientSECRETtest'
    
    #Usando a função para requerir o token, futuramente adicionar memoria em cache para armazenar o token momentaneamente
    token = get_token(client_id=client_id, client_secret=client_secret)
    #usando a função que requere os dados em JSON da API, futuramente adicinar uma tabela no banco de dados para salvar o JSON em multi-tenant, para não requisitar todas as vezes
    acount_id = 'conta-tenant-01'
    extract_API_data = get_extract_data(acess_token=token, acount_id=acount_id)
    return extract_API_data