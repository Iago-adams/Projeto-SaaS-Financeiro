from flask import render_template, request, current_app
from werkzeug.exceptions import HTTPException

def registar_erros(app):
    
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html')
    

    #essa erro significa que o sistema identificou, mas bloqueou a requisição (banco, ceo)
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html')
    

    #usar esse erro para os decorators, ex: ceo_required
    @app.errorhandler(401)
    def unauthorized_error(error):
        return render_template('errors/401.html')