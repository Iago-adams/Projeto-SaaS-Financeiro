#Requerir os dados da API
from ..services.extract_api import get_token, get_extract_data
from ..services.encryption import decrypt
from ..models import Company
import os
from dotenv import load_dotenv

def _get_decrypted_client_keys(account_id):
    company = Company.query.get_or_404(account_id)
    encrpClientId = company.secrets.client_id
    encrpClientSecret = company.secrets.client_secret
    return [decrypt(encrpClientId), decrypt(encrpClientSecret)]

def get_financial_JSON(account_id, agency_id):#Para a aplicação prática precisa passar o acount_id
    #pegar a client id e a client secret descriptografadas
    client_keys = _get_decrypted_client_keys(account_id)
    
    #Insira as credenciais do usuario aqui, futuramente aqui estara a função de descriptografar e puxar do banco de dados, no momento só estão Strings quaisquer para teste com a API mock
    #client_id = 'clientIDtest'
    #client_secret = 'clientSECRETtest'
    
    #Usando a função para requerir o token, futuramente adicionar memoria em cache para armazenar o token momentaneamente
    token = get_token(client_id=client_keys[0], client_secret=client_keys[1])
    #usando a função que requere os dados em JSON da API, futuramente adicinar uma tabela no banco de dados para salvar o JSON em multi-tenant, para não requisitar todas as vezes
    #account_id = 'conta-tenant-01'
    appKey = os.getenv('APP_KEY')
    extract_API_data = get_extract_data(acess_token=token, account_id=account_id, agency_id=agency_id, app_key=appKey)
    return extract_API_data