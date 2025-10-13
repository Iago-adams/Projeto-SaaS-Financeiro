#gerar a chave de criptografia

from cryptography.fernet import Fernet

chave = Fernet.generate_key()

print(f"Chave de Criptografia Gerada: {chave.decode()}")