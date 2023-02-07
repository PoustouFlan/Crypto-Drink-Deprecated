import requests
from data.models import *

def get_user(user):
    url = f"https://cryptohack.org/api/user/{user}/"
    request = requests.get(url)
    assert request.status_code == 200, (
        f"Impossible d'obtenir les informations concernant {user}. "
        "Le nom d'utilisateur est-il bien correct ?"
    )
    json = request.json()
    assert 'user_count' in json, (
        f"Erreur {json['code']}: {json['message']}"
    )
    return json
