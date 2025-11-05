from cryptography.fernet import Fernet
from .. import config

ENCRYPTION_KEY = config.ENCRYPTION_KEY
_FERNET_CIPHER = Fernet(ENCRYPTION_KEY.encode('utf-8'))

def encrypt(data: str):
    encryptedData = _FERNET_CIPHER.encrypt(data.encode('utf-8'))
    return encryptedData.decode('utf-8')

def decrypt(data: str):
    desencryptedData = _FERNET_CIPHER.decrypt(data)
    return desencryptedData