from flask import Blueprint, render_template, jsonify


main_bp = Blueprint(
    'main', 
    __name__,  
    template_folder='./templates'
    )

#Rota de login de usuário
@main_bp.route('/', methods=['GET', 'POST'])
def homepage():
    
    return render_template('homepage.html')


#Health chech testa se o projeto está rodando corretamente
@main_bp.route('/health', methods=['GET', 'POST'])
def health_check():
    return jsonify({"status": "online"}), 200