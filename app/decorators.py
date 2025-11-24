from .models import User
from flask_login import current_user
from flask import abort
import os

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
    def wrapper(*args, **kwargs):
        
        if not current_user.is_authenticated:
            abort(401)

        #pega o caminho do arquivo
        path = os.getcwd()

        #pega o caminho e no dirname pega só as pastas em que eles está contido, dps o basename pega o último arquivo, que será a pasta
        directory = os.path.basename(os.path.dirname(path))
        print(directory)

        permissions = current_user.membership.role.permissions #é para pegar as permissões do usuário
        print(permissions.codename)

        if permissions is None: #erro 500 ,só Deus sabe o que ocasiona o problema
            abort(500)

        elif directory == permissions.codename:
            return f(*args, **kwargs)
        
        else:
            abort(403)

        return wrapper