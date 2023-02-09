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

CATEGORY_LINK = {
    "Introduction" : "https://cryptohack.org/challenges/introduction/",
    "General" : "https://cryptohack.org/challenges/general/",
    "Mathematics" : "https://cryptohack.org/challenges/maths/",
    "Symmetric Ciphers" : "https://cryptohack.org/challenges/aes/",
    "RSA" : "https://cryptohack.org/challenges/rsa/",
    "Diffie-Hellman" : "https://cryptohack.org/challenges/diffie-hellman/",
    "Elliptic Curves" : "https://cryptohack.org/challenges/ecc/",
    "Hash Functions" : "https://cryptohack.org/challenges/hashes/",
    "Crypto on the Web" : "https://cryptohack.org/challenges/web/",
    "Misc" : "https://cryptohack.org/challenges/misc/",
    "Post-Quantum" : "https://cryptohack.org/challenges/post-quantum/",
    "CTF Archive" : "https://cryptohack.org/challenges/ctf-archive/",
}
