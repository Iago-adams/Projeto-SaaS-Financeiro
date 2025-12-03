import requests
import os
from dotenv import load_dotenv
from ..services.encryption import decrypt
from ..models import Secrets

load_dotenv()

# URLs
EXTRACT_BASE_URL = 'https://api.hm.bb.com.br/extratos/v1/conta-corrente'
OAUTH_TOKEN_URL = 'https://oauth.hm.bb.com.br/oauth/token'

def _get_mock_data():
    print("--- ⚠️ ATIVANDO MOCK DATA COM SALDOS ---")
    return {
        "listaLancamento": [
            # Dia 20: Entrada de 15k. Saldo foi para 50k.
            {"dataLancamento": "20042025", "textoDescricaoHistorico": "RECEBIMENTO CLIENTE A", "valorLancamento": 15000.00, "indicadorSinalLancamento": "C", "indicadorTipoLancamento": "1"},
            {"dataLancamento": "20042025", "textoDescricaoHistorico": "Saldo do dia", "valorLancamento": 50000.00, "indicadorSinalLancamento": "C", "indicadorTipoLancamento": "S"},

            # Dia 22: Pagamento de 1.2k. Saldo caiu.
            {"dataLancamento": "22042025", "textoDescricaoHistorico": "PGTO SERVIDOR AWS", "valorLancamento": 1200.50, "indicadorSinalLancamento": "D", "indicadorTipoLancamento": "1"},
            {"dataLancamento": "22042025", "textoDescricaoHistorico": "Saldo do dia", "valorLancamento": 48799.50, "indicadorSinalLancamento": "C", "indicadorTipoLancamento": "S"},

            # Dia 25: Venda de 3.5k. Saldo subiu.
            {"dataLancamento": "25042025", "textoDescricaoHistorico": "VENDA ASSINATURA SAAS", "valorLancamento": 3500.00, "indicadorSinalLancamento": "C", "indicadorTipoLancamento": "1"},
            {"dataLancamento": "25042025", "textoDescricaoHistorico": "Saldo do dia", "valorLancamento": 52299.50, "indicadorSinalLancamento": "C", "indicadorTipoLancamento": "S"},

            # Dia 05: Pagamento 4k. Saldo caiu.
            {"dataLancamento": "05052025", "textoDescricaoHistorico": "ALUGUEL ESCRITORIO", "valorLancamento": 4000.00, "indicadorSinalLancamento": "D", "indicadorTipoLancamento": "1"},
            {"dataLancamento": "05052025", "textoDescricaoHistorico": "Saldo do dia", "valorLancamento": 48299.50, "indicadorSinalLancamento": "C", "indicadorTipoLancamento": "S"},

            # Dia 15: Investimento 5k. Saldo caiu (saiu da conta corrente).
            {"dataLancamento": "15052025", "textoDescricaoHistorico": "INVESTIMENTO CDB", "valorLancamento": 5000.00, "indicadorSinalLancamento": "D", "indicadorTipoLancamento": "1"},
            {"dataLancamento": "15052025", "textoDescricaoHistorico": "Saldo do dia", "valorLancamento": 43299.50, "indicadorSinalLancamento": "C", "indicadorTipoLancamento": "S"}
        ]
    }

def _get_decrypted_client_keys(account_id):
    try:
        secrets = Secrets.query.filter_by(account_id=str(account_id)).first()
        if not secrets:
            return None
        return [decrypt(secrets.client_id), decrypt(secrets.client_secret)]
    except Exception:
        return None

def get_token(client_id, client_secret):
    payload = {'grant_type': 'client_credentials'} 
    try:
        # Timeout curto para não travar o site se o BB estiver lento
        response = requests.post(OAUTH_TOKEN_URL, data=payload, auth=(client_id, client_secret), verify=True, timeout=5)
        if response.status_code == 200:
            return response.json().get('access_token')
    except Exception:
        pass
    return None

def get_financial_JSON(account_id, agency_id):
    print(f"--- DATA FETCHER: Iniciando busca híbrida para Conta {account_id} ---")

    # tentativa de acessar os dados da API sandbox
    try:
        keys = _get_decrypted_client_keys(account_id)
        if keys:
            token = get_token(keys[0], keys[1])
            
            if token:
                appKey = os.getenv('APP_KEY')
                ag = str(agency_id).lstrip('0')
                cc = str(account_id).lstrip('0')
                
                url = f"{EXTRACT_BASE_URL}/agencia/{ag}/conta/{cc}"
                
                # Header MCI da conta 1348
                mci_header = '178961031' if cc == '1348' else 'teste'
                
                headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json',
                    'x-br-com-bb-ipa-mciteste': mci_header
                }
                
                #datas dos dados da API
                params = {
                    'gw-dev-app-key': appKey,
                    'quantidadeRegistroPaginaSolicitacao': 200
                }
                if "hm.bb.com.br" in EXTRACT_BASE_URL:
                    params['dataInicioSolicitacao'] = '20042025' 
                    params['dataFimSolicitacao'] = '19052025'

                print(f"--- TENTANDO CONEXÃO API BB... ---")
                # Timeout de 8 segundos. Se demorar mais que isso, aborta e vai pro Mock.
                response = requests.get(url, headers=headers, params=params, verify=True, timeout=8)
                
                if response.status_code == 200:
                    print("--- SUCESSO: Dados obtidos! ---")
                    return response.json()
                else:
                    print(f"--- FALHA API ({response.status_code}): {response.text} ---")
                    # FALHA NA RESPOSTA -> VAI PRO MOCK
            else:
                print("--- TOKEN FALHOU ---")
                # SEM TOKEN -> VAI PRO MOCK
        else:
            print("--- CHAVES NÃO ENCONTRADAS ---")
            # SEM CHAVES -> VAI PRO MOCK

    except Exception as e:
        # AQUI QUE O SEU ERRO DE TIMEOUT É CAPTURADO
        print(f"--- EXCEÇÃO NA API (Timeout/Erro): {e} ---")
        # FALHA DE CONEXÃO -> VAI PRO MOCK

    # caso não consiga requerir os dados do banco do brasil ele puxa aqui dados falsos pra fingir que ta tudo certo :)
    return _get_mock_data()