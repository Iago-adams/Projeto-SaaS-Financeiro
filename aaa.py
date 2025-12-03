import requests
from datetime import datetime, timedelta
import time

# --- SUAS CREDENCIAIS ---
CLIENT_ID = "eyJpZCI6ImM1MzIwYjUtOTllZC00MWEyLTgwZTEtYjFmNTMyIiwiY29kaWdvUHVibGljYWRvciI6MCwiY29kaWdvU29mdHdhcmUiOjE2MzYxNSwic2VxdWVuY2lhbEluc3RhbGFjYW8iOjF9" 
CLIENT_SECRET = "eyJpZCI6IjU4NGMzZDYtNjQzOC00NTZkLTkzNGItN2M0MThjNTk0ODQ5IiwiY29kaWdvUHVibGljYWRvciI6MCwiY29kaWdvU29mdHdhcmUiOjE2MzYxNSwic2VxdWVuY2lhbEluc3RhbGFjYW8iOjEsInNlcXVlbmNpYWxDcmVkZW5jaWFsIjozLCJhbWJpZW50ZSI6ImhvbW9sb2dhY2FvIiwiaWF0IjoxNzY0NTE5MzE1NTQwfQ"
APP_KEY = "a68367e991a0490d98d2c02befe6b1b4"

# Configuração da Conta 1348 (Compatível com seu escopo)
AGENCIA = "1505"
CONTA = "1348"
MCI = "178961031"

def gerar_token():
    url = "https://oauth.hm.bb.com.br/oauth/token"
    payload = {'grant_type': 'client_credentials'} 
    try:
        resp = requests.post(url, data=payload, auth=(CLIENT_ID, CLIENT_SECRET), verify=True)
        if resp.status_code == 200:
            return resp.json()['access_token']
    except:
        pass
    print("❌ Falha ao gerar token inicial.")
    return None

def scan_datas():
    print("--- 🕵️ INICIANDO O ARQUEÓLOGO DE DADOS ---")
    print("Vasculhando o servidor do BB em busca de qualquer transação perdida...")

    token = gerar_token()
    if not token: return

    # Configuração da Requisição
    url = f"https://api.hm.bb.com.br/extratos/v1/conta-corrente/agencia/{AGENCIA}/conta/{CONTA}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'x-br-com-bb-ipa-mciteste': MCI
    }

    # DATA INICIAL: 01/01/2023
    data_atual = datetime(2023, 1, 1)
    data_hoje = datetime.now()

    encontrou = False

    # LOOP: Avança de 30 em 30 dias
    while data_atual < data_hoje:
        # Define o fim da janela (Data Atual + 29 dias)
        data_fim = data_atual + timedelta(days=29)
        
        # Formata para string DDMMAAAA
        str_inicio = data_atual.strftime("%d%m%Y")
        str_fim = data_fim.strftime("%d%m%Y")

        params = {
            'gw-dev-app-key': APP_KEY,
            'dataInicioSolicitacao': str_inicio,
            'dataFimSolicitacao': str_fim,
            'quantidadeRegistroPaginaSolicitacao': 200
        }

        print(f"🔎 Testando janela: {str_inicio} até {str_fim}...", end="\r")

        try:
            resp = requests.get(url, headers=headers, params=params, verify=True)
            
            if resp.status_code == 200:
                json_data = resp.json()
                # Verifica se a lista não está vazia
                lista = json_data.get('listaLancamento', [])
                if lista and len(lista) > 0:
                    print(f"\n\n🏆 EUREKA! DADOS ENCONTRADOS!")
                    print(f"📅 Período com dados: {str_inicio} a {str_fim}")
                    print(f"💰 Quantidade de lançamentos: {len(lista)}")
                    print("--- Copie essas datas para o seu código! ---")
                    encontrou = True
                    break # Para o loop
            elif resp.status_code == 401:
                # Se o token expirar no meio do loop, gera outro
                token = gerar_token()
                headers['Authorization'] = f'Bearer {token}'
            
        except Exception as e:
            print(f"\nErro de conexão: {e}")

        # Avança para o próximo mês
        data_atual = data_atual + timedelta(days=30)
        # time.sleep(0.1) # Pequena pausa para não travar o terminal

    if not encontrou:
        print("\n\n❌ VARREDURA COMPLETA: NENHUM DADO ENCONTRADO.")
        print("Conclusão: O ambiente Sandbox para esta conta está 100% vazio/limpo.")
        print("Solução: Use o Mock Data.")

if __name__ == "__main__":
    scan_datas()