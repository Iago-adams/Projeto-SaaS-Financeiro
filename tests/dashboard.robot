*** Settings ***
Documentation     Testa o endpoint de KPIs do Dashboard
Library           RequestsLibrary
Library           Collections

*** Variables ***
${BASE_URL}                 http://localhost:5000
${DASHBOARD_API_ENDPOINT}   /dashboard/kpis

*** Test Cases ***
Validar KPIs Calculados do Dashboard
    [Tags]              API    Dashboard    Lógica
    [Documentation]     Valida se a API de KPIs retorna os cálculos corretos
    ...                 baseados no mock da 'conta-tenant-01'.

    Create Session          api_session      ${BASE_URL}
    ${response} =           GET On Session   api_session      ${DASHBOARD_API_ENDPOINT}

    Status Should Be        OK               ${response}
    
    # Validação do tipo de conteúdo (JSON)
    ${content_type} =       Get From Dictionary    ${response.headers}    Content-Type
    Should Contain          ${content_type}        application/json

    # Validação dos dados
    ${kpis} =               Set Variable     ${response.json()}
    Dictionary Should Contain Key    ${kpis}    total_revenue
    Dictionary Should Contain Key    ${kpis}    total_expenses
    Dictionary Should Contain Key    ${kpis}    current_balance

    # Valida os valores (do MOCK_DATA)
    ${revenue} =            Get From Dictionary    ${kpis}    total_revenue
    Should Be Equal As Numbers     ${revenue}     25000.00

    ${expenses} =           Get From Dictionary    ${kpis}    total_expenses
    Should Be Equal As Numbers     ${expenses}    -8500.00

    ${balance} =            Get From Dictionary    ${kpis}    current_balance
    Should Be Equal As Numbers     ${balance}     16500.00