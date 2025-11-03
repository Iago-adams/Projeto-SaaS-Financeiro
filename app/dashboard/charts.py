#Processa o JSON em um grafico
import pandas as pd
import plotly.express as px
import plotly.io as pio

def _normalize_JSON_transactions(JSON):
    #Normalizando o JSON(necessário pois o JSON está aninhado)
    JSON_normalized = pd.json_normalize(
        JSON,
        record_path='transactions'
    )
    
    #Transformando a coluna de data em datetime, e ordenando para criação de gráficos
    JSON_normalized['completedAt'] = pd.to_datetime(JSON_normalized['completedAt'])
    JSON_normalized = JSON_normalized.sort_values(by=['completedAt'])
    
    return JSON_normalized

def generate_lineGraph_extract(extract_API_data):
    #Normalizar os dados
    exctract_data_normalized = _normalize_JSON_transactions(extract_API_data)
    
    #configuração do gráfico linear
    fig_extract_data_line = px.line(
        exctract_data_normalized,
        x='completedAt',
        y='amount',
        
        # 1. Título e Labels (Nomes dos Eixos)
        title='Fluxo de Caixa (Receitas vs. Despesas)',
        labels={
            'completedAt': 'Data da Transação',  # Novo nome para o eixo X
            'amount': 'Valor (R$)'             # Novo nome para o eixo Y
        },
        
        # 2. Template Visual
        template='plotly_white', # Um template mais limpo que o padrão
        
        # 3. Marcadores e Dados de Hover
        markers=True,  # Garante que os pontos de dados sejam visíveis
        hover_data={
            # Adiciona a descrição e o tipo ao tooltip (quando passa o mouse)
            'description': True, 
            'type': True,
            # Formata o 'amount' no hover para 2 casas decimais
            'amount': ':.2f',
            # Formata a data no hover (opcional, mas recomendado)
            'completedAt': '|%d/%m/%Y %H:%M' 
        }
    )

    # 4. Polimento com update_layout (Formatação de Moeda e Linha Zero)
    fig_extract_data_line.update_layout(
        
        # Formata o Eixo Y para exibir como moeda (BRL)
        yaxis_tickprefix='R$ ',  # Adiciona "R$ " antes do valor
        yaxis_tickformat=',.2f', # Formato: separador de milhar e 2 casas decimais
        
        # Adiciona uma linha de referência horizontal no Y=0
        # Essencial para gráficos financeiros para separar ganhos de perdas
        shapes=[
            dict(
                type='line',
                yref='y', y0=0,
                xref='paper', x0=0, x1=1, # Linha que atravessa 100% da largura
                line=dict(color='Gray', width=1.5, dash='dash')
            )
        ],
        
        # Ajustes de fonte (opcional, para profissionalizar)
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="#333333"
        )
    )

    # Conversão para HTML
    graph_extract_data_line_html = pio.to_html(fig_extract_data_line, full_html=False, include_plotlyjs='cdn')
    
    return graph_extract_data_line_html