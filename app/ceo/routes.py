from flask import Blueprint
from flask_login import login_required, current_user

ceo_bp = Blueprint('ceo', __name__, url_prefix='/ceo', template_folder='./templates')

