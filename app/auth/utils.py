from app import mail, db
from flask_mail import Message
from flask import url_for
from app.models import Role, CompanyMembers, Permissions, RolePermissions
import random, string
from werkzeug.security import generate_password_hash
import re, pwnedpasswords
from typing import Tuple

#função para enviar a primeira senha (gerada aleatoriamente) para o email corporativo
def reset_password(target):
    
    link = url_for('auth.reset_password', id=target.id)

    msg = Message(
        subject='Credencial de acesso',
        recipients=target.email,
        body=f'''Siga o link para a redefinição de sua senha
                {link}
                Caso não tenha solicitado ignore esse email.'''
    )

    mail.send(msg)

def send_first_password(target, password):

    link = url_for('auth.reset_password', id=target.id)

    msg = Message(
        subject='Credencial de acesso',
        recipients=target.email,
        body=f'''Você está com a senha temporária: {password}.
                Para sua segurança redefina sua senha. 
                Siga o link abaixo para a redefinição de senha
                {link}'''
    )

    mail.send(msg)

#recebe o company id e user id para definir que o usuário terá a role CEO
def create_ceo(c_id, u_id):
    ceo = Role(
        name='CEO',
        company_id=c_id
    )

    perms = Permissions.query.all()

    for perm in perms:
        role_perm = RolePermissions(
            permission=perm
        )
        ceo.permissions.append(role_perm)
    
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
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    


def validate_password_complexity(password: str) -> Tuple[bool, str]:
    """
    Valida a senha contra os requisitos mínimos de complexidade.
    Retorna (True, None) se válida, ou (False, "mensagem de erro") se inválida.
    """
    
    # Requisito 1: Comprimento Mínimo (Crucial para segurança)
    MIN_LENGTH = 12
    if len(password) < MIN_LENGTH:
        return False, f"A senha deve ter no mínimo {MIN_LENGTH} caracteres."

    # Requisito 2: Letra Maiúscula
    if not re.search(r"[A-Z]", password):
        return False, "A senha deve conter pelo menos uma letra maiúscula."

    # Requisito 3: Letra Minúscula
    if not re.search(r"[a-z]", password):
        return False, "A senha deve conter pelo menos uma letra minúscula."

    # Requisito 4: Número
    if not re.search(r"\d", password):
        return False, "A senha deve conter pelo menos um número."

    # Requisito 5: Caractere Especial (ajuste o conjunto conforme necessário)
    if not re.search(r"[!@#$%&?]", password):
        return False, "A senha deve conter pelo menos um caractere especial."

    # Todos os requisitos atendidos
    return True, None


def validate_password_policy(password: str) -> Tuple[bool, str]:
    """
    Valida a política de senha completa (Complexidade + Exposição).
    """
    
    # 1. Validar Complexidade (usando a função anterior)
    is_complex, message = validate_password_complexity(password)
    if not is_complex:
        return False, message

    # 2. Validar Exposição (Check de Vazamentos)
    # Esta verificação é anônima e rápida.
    exposure_count = pwnedpasswords.check(password)
    
    if exposure_count > 0:
        return False, f"Esta senha é insegura, pois já apareceu em {exposure_count} vazamentos de dados conhecidos. Por favor, escolha outra."

    # Senha aprovada
    return True, None
