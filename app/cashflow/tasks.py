#Enviar o pdf em segundo plano
import threading
from flask import current_app
from flask_mail import Message
from .. import mail

def send_email_async(app, msg):
    """Função interna que roda na Thread"""
    with app.app_context():
        try:
            mail.send(msg)
            print("Email enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar email: {e}")

def send_reports_background(pdf_bytes, recipients_ids, company_name):
    """
    Prepara o email e lança uma Thread para envio em segundo plano.
    """
    # Obter a app atual antes de lançar a thread (contexto do Flask)
    app = current_app._get_current_object()
    
    # Nota: recipients_ids aqui deveria ser uma lista de EMAILS, não IDs.
    # Vou assumir que o Service já vai me mandar os e-mails ou objetos User.
    # Se vierem IDs, precisaríamos buscar no banco aqui, mas é melhor o service resolver.
    
    if not recipients_ids:
        print("Nenhum destinatário encontrado.")
        return

    msg = Message(
        subject=f"Relatório Financeiro - {company_name}",
        recipients=recipients_ids, # Lista de strings ['email1@teste.com', 'email2@...']
        body=f"Olá,\n\nSegue em anexo o relatório atualizado de fluxo de caixa da {company_name}.\n\nAtenciosamente,\nSaaS Financeiro"
    )
    
    # Anexa o PDF
    msg.attach(
        filename="relatorio_financeiro.pdf",
        content_type="application/pdf",
        data=pdf_bytes
    )
    
    # Inicia a thread
    thread = threading.Thread(target=send_email_async, args=(app, msg))
    thread.start()
    
    return True