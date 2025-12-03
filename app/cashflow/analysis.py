import pandas as pd
import plotly.express as px
import plotly.io as pio

def normalize_JSON_transactions(JSON):
    # Segurança básica
    if not JSON or 'listaLancamento' not in JSON:
        return pd.DataFrame(columns=['completedAt', 'amount', 'description', 'type'])

    # 1. Normaliza tudo
    df_raw = pd.json_normalize(JSON, record_path='listaLancamento')

    # --- FILTRAGEM INVERTIDA: SÓ QUEREMOS O SALDO ---
    # Procuramos por linhas onde a descrição contém "Saldo"
    # ou onde o tipo NÃO seja '1' (transação).
    
    if 'textoDescricaoHistorico' in df_raw.columns:
        # Filtra apenas linhas que tem "Saldo" no nome
        JSON_normalized = df_raw[df_raw['textoDescricaoHistorico'].str.contains("Saldo", case=False, na=False)].copy()
    else:
        # Fallback: Se não tiver descrição, tentamos pegar tudo que NÃO é transação tipo 1
        if 'indicadorTipoLancamento' in df_raw.columns:
             JSON_normalized = df_raw[df_raw['indicadorTipoLancamento'] != '1'].copy()
        else:
             JSON_normalized = df_raw.copy()

    if JSON_normalized.empty:
         return pd.DataFrame(columns=['completedAt', 'amount', 'description', 'type'])

    # 2. Renomeando
    JSON_normalized = JSON_normalized.rename(columns={
        'dataLancamento': 'completedAt',
        'valorLancamento': 'amount',
        'textoDescricaoHistorico': 'description',
        'indicadorSinalLancamento': 'type'
    })

    # 3. Data
    JSON_normalized['completedAt'] = pd.to_datetime(
        JSON_normalized['completedAt'], 
        format='%d%m%Y', 
        errors='coerce'
    )

    # 4. Sinais (Saldo Devedor vs Credor)
    # Se o saldo estiver negativo (D), multiplica por -1
    if 'type' in JSON_normalized.columns:
        JSON_normalized['amount'] = JSON_normalized.apply(
            lambda row: row['amount'] * -1 if row['type'] == 'D' else row['amount'], 
            axis=1
        )

    # Ordena por data (Essencial para a linha do tempo)
    JSON_normalized = JSON_normalized.sort_values(by=['completedAt'])
    
    # Se houver mais de um saldo no mesmo dia, pegamos o último (Saldo Fechado)
    JSON_normalized = JSON_normalized.drop_duplicates(subset=['completedAt'], keep='last')

    return JSON_normalized

def calculate_kpis_from_dataframe(df):
    """
    KPIs para Saldo são diferentes.
    Não somamos tudo (senão soma saldo do dia 1 + dia 2...), pegamos o último.
    """
    if df.empty:
        return {"total_revenue": 0, "total_expenses": 0, "current_balance": 0}

    # O Saldo Atual é simplesmente o último registro da linha do tempo
    current_balance = df['amount'].iloc[-1]
    
    # Receita e Despesa não dá para calcular só olhando a linha de saldo
    # (Precisaríamos das transações). Então retornamos 0 ou mantemos a lógica antiga
    # se você passar o dataframe COMPLETO (sem filtro) para cá. 
    # Para simplificar e não quebrar o front, retornamos o saldo atual.
    
    return {
        "total_revenue": 0, # Não calculável apenas com linhas de saldo
        "total_expenses": 0,
        "current_balance": current_balance
    }

def get_extract_figure(exctract_data_normalized):
    if exctract_data_normalized.empty:
        fig = px.line(title="Sem histórico de saldo.")
        fig.update_layout(template='plotly_white', xaxis={'visible':False}, yaxis={'visible':False})
        return fig

    # Gráfico de ÁREA (Fica mais bonito para Saldo)
    fig = px.area(
        exctract_data_normalized,
        x='completedAt',
        y='amount',
        title='Evolução do Saldo Bancário',
        labels={'completedAt': 'Data', 'amount': 'Saldo (R$)'},
        template='plotly_white',
        markers=True
    )

    fig.update_layout(
        yaxis_tickprefix='R$ ',
        yaxis_tickformat=',.2f',
        hovermode="x unified",
        font=dict(family="Segoe UI, sans-serif", size=12, color="#333"),
        # Adiciona um padding no eixo Y para a linha não colar no teto/chão
        yaxis=dict(autorange=True) 
    )
    
    # Cor da linha/área baseada no saldo atual
    saldo_atual = exctract_data_normalized['amount'].iloc[-1]
    cor = '#00C851' if saldo_atual >= 0 else '#ff4444' # Verde ou Vermelho
    
    fig.update_traces(line_color=cor, fill='tozeroy') # Preenche até o zero

    return fig

def generate_lineGraph_extract_html(exctract_data_normalized):
    fig = get_extract_figure(exctract_data_normalized)
    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')