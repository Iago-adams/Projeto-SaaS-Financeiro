from app import mail, db
from flask_mail import Message
from flask import url_for
from models import Role, CompanyMembers

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

def create_ceo(c_id, u_id):
    ceo = Role(
        name='CEO',
        company_id=id
    )
    db.session.add(ceo)
    db.session.commit()
    
    member = CompanyMembers(
        user_id=u_id,
        company_id = c_id,
        role_id = ceo.id
    )

    db.session.add(member)
    db.session.commit()