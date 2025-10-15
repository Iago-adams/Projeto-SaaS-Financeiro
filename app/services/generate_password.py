import random, string

def generate_password():
    ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))