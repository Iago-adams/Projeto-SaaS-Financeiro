from app import mail
from flask_mail import Message
from flask import url_for
from models import User

def send_first_password(target):
    
    link = url_for('auth.reset_password')

    msg = Message(
        subject='Credencial de acesso'
    )

    return