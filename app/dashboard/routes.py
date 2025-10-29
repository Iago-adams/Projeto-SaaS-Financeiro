from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_user, logout_user, login_required
from ..services.extract_api import get_token, get_extract_data
from ..decorators import ceo_required
import pandas as pd
import json

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
    exctract_data_normalazed = pd.json_normalize(
        extract_API_data,
        record_path='transactions'
    )
    exctract_data_normalazed['completedAt'] = pd.to_datetime(exctract_data_normalazed['completedAt'])
    print(exctract_data_normalazed)
    return render_template('dashboard.html')