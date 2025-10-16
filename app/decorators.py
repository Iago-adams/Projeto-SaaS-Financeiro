from .models import User
from flask_login import current_user

def ceo_required(f):
    def func():
        if current_user.