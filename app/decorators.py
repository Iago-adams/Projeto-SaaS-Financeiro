from .models import User
from flask_login import current_user
from flask import abort

def ceo_required(f):
    def wrapper():
        if current_user.is_authenticated:
            if current_user.membership.role != "CEO":
                abort(401)
            else:
                f()
                
    return wrapper
