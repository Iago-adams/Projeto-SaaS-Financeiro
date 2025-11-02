from app import mail, db
from flask_mail import Message
from flask import url_for
from app.models import Role, CompanyMembers, Permissions
import random, string

#função para enviar a primeira senha (gerada aleatoriamente) para o email corporativo
def send_first_password(target):
    
    link = url_for('auth.reset_password', id=target.id)

    msg = Message(
        subject='Credencial de acesso',
        recipients=target.email,
        body=f'''Siga o link para a redefinição de sua senha
                {link}
                Caso já tenha '''
    )

    return

#recebe o company id e user id para definir que o usuário terá a role CEO
def create_ceo(c_id, u_id):
    ceo = Role(
        name='CEO',
        company_id=c_id
    )

    for perms in Permissions.query.all():
        ceo.permissions.apend(perms)
    
    db.session.add(ceo)
    db.session.commit()

    member = CompanyMembers(
        user_id=u_id,
        company_id = c_id,
        role_id = ceo.id
    )

    db.session.add(member)
    db.session.commit()

def generate_password():
    ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))