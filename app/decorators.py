from .models import User

def ceo_required(f):
    def func():
