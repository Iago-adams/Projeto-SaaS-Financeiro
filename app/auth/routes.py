from flask import Blueprint
from app.models import User
from forms import LoginForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/', methods=['GET', 'POST'])
def login():

    
    return