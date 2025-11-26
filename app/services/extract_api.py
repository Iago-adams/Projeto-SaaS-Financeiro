# rotas de requisição do json da api de estrato(no momento configurada para funcionar com a mock API)
import requests
from datetime import datetime

EXTRACT_BASE_URL = 'https://api.hm.bb.com.br/extratos/v1'
OAUTH_TOKEN_URL = 'https://oauth.hm.bb.com.br/oauth/token'

def get_token(client_id: str, client_secret: str, scope: str = "extratos.consultar"):
    #Url da api(no momento é a url do mock)
    #token_url = 'http://127.0.0.1:5001/oauth/token'
    
    #dados enviado para a API
    payload = {
        'grant_type': 'client_credentials',
        'scope': scope
    }
    
    #cabeçalho da requisição
    headers= {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    
    try:
        # faz a requisição com o endpoint
        response = requests.post(
            OAUTH_TOKEN_URL, 
            data=payload, 
            headers=headers,
            auth=(client_id, client_secret),
            verify=True
            )
        
        # caso o erro for HTTP ele lança o erro
        response.raise_for_status()
        
        #pega o json retorando pelo endpoint
        response_data = response.json()
        
        #busca pelo access token no json retornado pelo endpoint
        access_token = response_data.get('access_token')
        
        if not access_token:
            #Se cair nesse caso a conecção com o endpoint foi bem sucedida porém o acces token não esta presente na resposta da API
            raise Exception("Access token não encontrado")
        
        return access_token
    
    except requests.exceptions.RequestException as e:
        print(f'Erro de conexão ou HTTP ao obter token: {e}')
        if e.response is not None:
             print(f'Detalhe do erro: {e.response.text}')
        return None
    
def get_extract_data(acess_token: str, account_id: str, app_key: str, agency_id: str):
        #inserir aqui a url do endipoint da API
    #data_url = f'http://127.0.0.1:5001/contas/{account_id}/extrato'
    
    #remove os zeros a esquerda de acordo com o pedido pela documentação
    agencia_fmt = str(agency_id).lstrip('0')
    conta_fmt = str(account_id).lstrip('0')

    endpoint = f"{EXTRACT_BASE_URL}/conta-corrente/agencia/{agencia_fmt}/conta/{conta_fmt}"
    
    headers = {
        'Authorization': f'Bearer {acess_token}',
        'Content-Type': 'application/json',
        'x-br-com-bb-ipa-mci': 'teste'
    }
    
    params = {
        'gw-dev-app-key': app_key,
        'numeroPaginaSolicitacao': 1,
        'quantidadeRegistroPaginaSolicitacao': 200
    }
    
    try:
        response = requests.get(endpoint, headers=headers, params=params, verify=True)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados financeiros: {e}")
        if e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Resposta da API: {e.response.text}")
        return None