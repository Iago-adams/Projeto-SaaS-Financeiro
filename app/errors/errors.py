from flask import render_template, request, current_app, Blueprint
from werkzeug.exceptions import HTTPException

errors_bp = Blueprint(
    'errors',
    __name__,
    template_folder='./templates'
)


@errors_bp.app_errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
    
#essa erro significa que o sistema identificou, mas bloqueou a requisição (banco, ceo)
@errors_bp.app_errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403
    

#usar esse erro unauthorized (tipo login)
@errors_bp.app_errorhandler(401)
def unauthorized_error(error):
    return render_template('401.html'), 401

#erro quando o problema for o servidor
@errors_bp.app_errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500