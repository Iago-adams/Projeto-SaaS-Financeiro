from .models import User
from flask_login import current_user

def ceo_required(f):
    def func():
<<<<<<< HEAD
        if current_user.membership.role == ""
=======
        if current_user.
>>>>>>> e7729cb66c56b9a29352122f71d6d80053002669
