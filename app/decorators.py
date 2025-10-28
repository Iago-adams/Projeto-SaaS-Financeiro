from .models import User
from flask_login import current_user
from flask import abort


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
