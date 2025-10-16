# rotas de requisição do json da api de estrato(no momento configurada para funcionar com a mock API)
import requests

def get_token(client_id: str, client_secret: str):
    #Url da api(no momento é a url do mock)
    token_url = 'http://127.0.0.1:5001/oauth/token'
    
    #dados enviado para a API
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }
    
    #cabeçalho da requisição
    headers= {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    
    try:
        # faz a requisição com o endpoint
        response = requests.post(token_url, data=payload, headers=headers)
        
        # caso o erro for HTTP ele lança o erro
        response.raise_for_status()
        
        #pega o json retorando pelo endpoint
        response_data = response.json()
        
        #busca pelo access token no json retornado pelo endpointq
        access_token = response_data.get('access_token')
        
        if not access_token:
            #Se cair nesse caso a conecção com o endpoint foi bem sucedida porém o acces token não esta presente na resposta da API
            raise Exception("Access token não encontrado")
        
        return access_token
    
    except requests.exceptions.RequestException as e:
        #Se cair nesse caso o erro está relacionado ao HTTP ou a rede possivelmente
        print(f'Erro ao obter o acces token: {e}')
        return None
    
def get_extract_data():
    