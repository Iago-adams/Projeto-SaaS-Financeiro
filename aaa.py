import requests

# --- SUAS CREDENCIAIS ---
CLIENT_ID = "eyJpZCI6ImM1MzIwYjUtOTllZC00MWEyLTgwZTEtYjFmNTMyIiwiY29kaWdvUHVibGljYWRvciI6MCwiY29kaWdvU29mdHdhcmUiOjE2MzYxNSwic2VxdWVuY2lhbEluc3RhbGFjYW8iOjF9" 
CLIENT_SECRET = "eyJpZCI6IjU4NGMzZDYtNjQzOC00NTZkLTkzNGItN2M0MThjNTk0ODQ5IiwiY29kaWdvUHVibGljYWRvciI6MCwiY29kaWdvU29mdHdhcmUiOjE2MzYxNSwic2VxdWVuY2lhbEluc3RhbGFjYW8iOjEsInNlcXVlbmNpYWxDcmVkZW5jaWFsIjozLCJhbWJpZW50ZSI6ImhvbW9sb2dhY2FvIiwiaWF0IjoxNzY0NTE5MzE1NTQwfQ"
APP_KEY = "a68367e991a0490d98d2c02befe6b1b4"
# DADOS DA CONTA 1348 (Específica para extrato-info)
CONTA = "1348"
AGENCIA = "1505"
MCI = "178961031" # <--- ESTE É O MCI EXCLUSIVO DA CONTA 1348

def teste_conta_1348():
    print("--- 🕵️ TESTE FINAL: CONTA 1348 ---")

    # 1. TOKEN
    url_token = "https://oauth.hm.bb.com.br/oauth/token"
    # Não mandamos scope para ele pegar o padrão (extrato-info)
    payload = {'grant_type': 'client_credentials'} 
    
    resp_token = requests.post(url_token, data=payload, auth=(CLIENT_ID, CLIENT_SECRET), verify=True)
    if resp_token.status_code != 200:
        print("❌ Erro Token:", resp_token.text)
        return
    
    token = resp_token.json()['access_token']
    print("✅ Token OK (extrato-info).")

    # 2. EXTRATO
    # URL da documentação (Sem /extrato no final)
    url = f"https://api.hm.bb.com.br/extratos/v1/conta-corrente/agencia/{AGENCIA}/conta/{CONTA}"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'x-br-com-bb-ipa-mciteste': MCI # Header correto da 1348
    }

    # Datas fixas de 2023 onde a documentação diz que tem dados
    params = {
        'gw-dev-app-key': APP_KEY,
        'dataInicioSolicitacao': '19042023',
        'dataFimSolicitacao': '23042023',
        'quantidadeRegistroPaginaSolicitacao': 200
    }

    print(f"📡 Request: {url}")
    print(f"🔑 Header MCI: {MCI}")
    
    resp = requests.get(url, headers=headers, params=params, verify=True)
    
    if resp.status_code == 200:
        print("\n🏆 SUCESSO! DADOS ENCONTRADOS:")
        print(resp.json())
    else:
        print(f"\n❌ Falha ({resp.status_code})")
        print("Resposta:", resp.text)

if __name__ == "__main__":
    teste_conta_1348()