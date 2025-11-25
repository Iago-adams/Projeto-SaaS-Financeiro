from .models import User
from flask_login import current_user
from flask import abort, request
import os
from functools import wraps

def ceo_required(f):
    def wrapper(*args, **kwargs):
        
        if not current_user.is_authenticated:
            abort(401)

        try:
            if current_user.membership.role != "CEO":
                abort(403)
        except AttributeError:
            #caso de pau no db, já não autoriza tbm q se foda, sistema bom é isso deu pau a culpa é do usuário
            abort(403)

        return f(*args, **kwargs)
    
    return wrapper

def permission_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        
        if not current_user.is_authenticated:
            abort(401)

        permissions = [p.codename for p in current_user.membership.role.permissions] #é para pegar as permissões do usuário
        print(permissions)

        if permissions == [] or permissions is None: #erro 500 ,só Deus sabe o que ocasiona o problema
            abort(500)

        elif request.blueprint in permissions:
            return f(*args, **kwargs)
        
        else:
            abort(403)

    return wrapper