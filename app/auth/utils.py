from app import mail, db
from flask_mail import Message
from flask import url_for
from app.models import Role, CompanyMembers, Permissions, RolePermissions
import random
import string
import re
import hashlib
import requests
from typing import Tuple
# Nota: werkzeug.security não estava sendo usado aqui, mas mantive caso você use no futuro
from werkzeug.security import generate_password_hash 

# --- Funções de Email ---

def reset_password(target):
    link = url_for('auth.reset_password', id=target.id, token=target.generate_token_password(), _external=True)

    msg = Message(
        subject='Credencial de acesso',
        recipients=[target.email],
        body=f'''Siga o link para a redefinição de sua senha
                {link}
                Caso não tenha solicitado ignore esse email.'''
    )

    mail.send(msg)

def send_first_password(target, password):
    link = url_for('auth.reset_password', id=target.id, token=target.generate_token_password(), _external=True)

    msg = Message(
        subject='Credencial de acesso',
        recipients=[target.email],
        body=f'''Você está com a senha temporária: {password}.
                Para sua segurança redefina sua senha. 
                Siga o link abaixo para a redefinição de senha
                {link}'''
    )

    mail.send(msg)

# --- Funções de Negócio / Roles ---

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
    # Gera uma senha aleatória de 6 caracteres para o primeiro acesso
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# --- Validação de Senha e Segurança ---

def get_pwned_count(password: str) -> int:
    """
    Verifica manualmente na API 'Have I Been Pwned' se a senha vazou.
    Usa k-Anonymity: envia apenas os 5 primeiros caracteres do hash SHA-1.
    """
    # 1. Hash SHA-1 e uppercase (requisito da API)
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    
    # 2. Divide hash (Prefixo para envio, Sufixo para checagem local)
    prefix, suffix = sha1password[:5], sha1password[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    
    try:
        # 3. Timeout de 2s para não travar a aplicação
        response = requests.get(url, timeout=2)
        
        if response.status_code != 200:
            return 0 # Fail Open (se API cair, permite cadastro)
            
        # 4. Verifica se o sufixo existe na resposta
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return int(count)
        
        return 0
        
    except requests.RequestException:
        return 0

def validate_password_complexity(password: str) -> Tuple[bool, str]:
    """
    Valida a senha contra os requisitos mínimos de complexidade.
    """
    
    MIN_LENGTH = 12
    if len(password) < MIN_LENGTH:
        return False, f"A senha deve ter no mínimo {MIN_LENGTH} caracteres."

    if not re.search(r"[A-Z]", password):
        return False, "A senha deve conter pelo menos uma letra maiúscula."

    if not re.search(r"[a-z]", password):
        return False, "A senha deve conter pelo menos uma letra minúscula."

    if not re.search(r"\d", password):
        return False, "A senha deve conter pelo menos um número."

    # Expandido para aceitar mais caracteres especiais comuns
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "A senha deve conter pelo menos um caractere especial."

    return True, None

def validate_password_policy(password: str) -> Tuple[bool, str]:
    """
    Valida a política de senha completa (Complexidade + Exposição).
    """
    
    # 1. Validar Complexidade
    is_complex, message = validate_password_complexity(password)
    if not is_complex:
        return False, message

    # 2. Validar Exposição (Usa a nova função manual)
    exposure_count = get_pwned_count(password)
    
    if exposure_count > 0:
        return False, f"Esta senha é insegura, pois já apareceu em {exposure_count} vazamentos de dados conhecidos. Por favor, escolha outra."

    return True, None