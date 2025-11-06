# run.py
from app import create_app, create_permissions

# Cria a instância principal do aplicativo
app = create_app()

# Agora, usa o "contexto" do app para executar
# tarefas que precisam do banco de dados
with app.app_context():
    print("Verificando e criando permissões...")
    create_permissions()
    print("Permissões verificadas.")

# Executa o servidor principal
if __name__ == "__main__":
    app.run(debug=True) # Use debug=True para desenvolvimento