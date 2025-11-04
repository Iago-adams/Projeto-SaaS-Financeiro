from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import sys

#apenas declarando, vai ser iniciado no init
ph = None

def 