import secrets
import string

def generate_ticket_code():
    characters = string.ascii_uppercase + string.digits

    return ''.join(
        secrets.choice(characters)
        for _ in range(14)
    )