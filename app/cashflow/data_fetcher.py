#Requerir os dados da API
from ..services.extract_api import get_token, get_extract_data
from ..services.encryption import decrypt
from ..models import Secrets
import os
from dotenv import load_dotenv

def _get_decrypted_client_keys(account_id):
    secrets = Secrets.query.filter_by(account_id=str(account_id)).first()
    if not secrets:
        print(f"--- ERRO: Segredos não encontrados para a conta {account_id} ---")
        return None
    
    return [decrypt(secrets.client_id), decrypt(secrets.client_secret)]

def get_financial_JSON(account_id, agency_id):
    print(f"--- DATA FETCHER: Iniciando para Conta {account_id} ---")

    #busca chaves no banco
    client_keys = _get_decrypted_client_keys(account_id)
    if not client_keys:
        return None
    
    #gera o Token
    token = get_token(client_id=client_keys[0], client_secret=client_keys[1])
    if not token:
        print("--- DATA FETCHER: Falha ao obter Token ---")
        return None

    #pega a App Key do .env
    appKey = os.getenv('APP_KEY')
    if not appKey:
        print("--- DATA FETCHER: APP_KEY não encontrada no .env ---")
        return None

    client_id_decrypted = "eyJpZCI6IjA2ZjA4YjQtNWVmYS00NjBjLTk0YiIsImNvZGlnb1B1YmxpY2Fkb3IiOjAsImNvZGlnb1NvZnR3YXJlIjoxNjMzMzUsInNlcXVlbmNpYWxJbnN0YWxhY2FvIjoxfQ" 
    client_secret_decrypted = "eyJpZCI6IjllMzQzNTMtZjI2NS00YWQxLWJhYjgtMzBiN2RmMDllNDk5MjYiLCJjb2RpZ29QdWJsaWNhZG9yIjowLCJjb2RpZ29Tb2Z0d2FyZSI6MTYzMzM1LCJzZXF1ZW5jaWFsSW5zdGFsYWNhbyI6MSwic2VxdWVuY2lhbENyZWRlbmNpYWwiOjIsImFtYmllbnRlIjoiaG9tb2xvZ2FjYW8iLCJpYXQiOjE3NjQ1MTU4OTAxMjB9"
    
    #busca os dados
    extract_API_data = get_extract_data(acess_token=token, account_id=account_id, agency_id=agency_id, app_key=appKey)
    
    return extract_API_data