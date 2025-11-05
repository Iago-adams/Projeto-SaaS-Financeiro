*** Settings ***
[Documentation]    Testes de Health Check para a API de Gerenciamento Financeiro
Library            RequestsLibrary

*** Variables ***
${BASE_URL}        http://127.0.0.1:5000    # Mude para a URL de produção/staging no Render se necessário

*** Test Cases ***
Verificar se a API está online
    [Documentation]    Este teste verifica o endpoint /health da aplicação.
    [Tags]             HealthCheck    API

    # Etapa 1: Criar a sessão (opcional, mas boa prática)
    Create Session    api_health    ${BASE_URL}

    # Etapa 2: Fazer a requisição GET para /health
    ${response}=    GET On Session    api_health    /health

    # Etapa 3: Validar a Resposta
    # Verificação 3.1: O Status Code deve ser 200 (OK)
    Should Be Equal As Strings    ${response.status_code}    200

    # Verificação 3.2: O conteúdo do JSON deve ser o esperado
    ${json_response}=    Set Variable    ${response.json()}
    Should Be Equal As Strings    ${json_response['status']}    online