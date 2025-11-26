from .models import User
from flask_login import current_user
from flask import abort, request
import os
from functools import wraps

def permission_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        route = request.blueprint
        
        if not current_user.is_authenticated:
            abort(401)

        if current_user.has_permission(route):
            return f(*args, **kwargs)
        
        else:
            abort(403)

    return wrapper