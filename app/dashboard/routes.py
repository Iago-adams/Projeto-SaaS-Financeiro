from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_user, logout_user, login_required
from ..services.extract_api import get_token, get_extract_data
from ..decorators import ceo_required
import pandas as pd
import plotly.express as px
import plotly.io as pio

dashboard_bp = Blueprint(
    'dashboard', 
    __name__,  
    template_folder='./templates'
    )

#Rota de login de usuário
@dashboard_bp.route('/', methods=['GET', 'POST'])
def dashboard():
    #Insira as credenciais do usuario aqui, futuramente aqui estara a função de descriptografar e puxar do banco de dados, no momento só estão Strings quaisquer para teste com a API mock
    client_id = 'clientIDtest'
    client_secret = 'clientSECRETtest'
    
    #Usando a função para requerir o token, futuramente adicionar memoria em cache para armazenar o token momentaneamente
    token = get_token(client_id=client_id, client_secret=client_secret)
    #usando a função que requere os dados em JSON da API, futuramente adicinar uma tabela no banco de dados para salvar o JSON em multi-tenant, para não requisitar todas as vezes
    acount_id = 'conta-tenant-01'
    extract_API_data = get_extract_data(acess_token=token, acount_id=acount_id)
    
    #Normalizando o JSON(necessário pois o JSON está aninhado)
    exctract_data_normalized = pd.json_normalize(
        extract_API_data,
        record_path='transactions'
    )
    
    #Transformando a coluna de data em datetime, e ordenando para criação de gráficos lineares
    exctract_data_normalized['completedAt'] = pd.to_datetime(exctract_data_normalized['completedAt'])
    exctract_data_normalized = exctract_data_normalized.sort_values(by=['completedAt'])
    
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

    # Conversão para HTML (seu código original está correto)
    graph_extract_data_line_html = pio.to_html(fig_extract_data_line, full_html=False, include_plotlyjs='cdn')

    return render_template('dashboard.html', graph_extract_line=graph_extract_data_line_html)