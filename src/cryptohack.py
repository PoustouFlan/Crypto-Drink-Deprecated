import requests
from typing import List
from dataclasses import dataclass
from datetime import datetime

strptime = lambda date: datetime.strptime(date, '%d %b %Y')

@dataclass
class Challenge:
    category: str
    date:     datetime
    name:     str
    points:   int
    solves:   int

    @classmethod
    def from_json(cls, json):
        json['date'] = strptime(json['date'])
        return cls(**json)

@dataclass
class User:
    country:           str
    first_bloods:      int
    joined:            datetime
    level:             int
    rank:              int
    score:             int
    solved_challenges: List[Challenge]
    user_count:        int
    username:          str
    website:           str

    @classmethod
    def from_json(cls, json):
        json['solved_challenges'] = list(map(
            lambda challenge: Challenge.from_json(challenge),
            json['solved_challenges']
        ))
        json['joined'] = strptime(json['joined'])
        return cls(**json)

def get_user(user):
    url = f"https://cryptohack.org/api/user/{user}/"
    request = requests.get(url)
    assert request.status_code == 200, (
        f"Impossible d'obtenir les informations concernant {user}. "
        "Le nom d'utilisateur est-il bien correct ?"
    )
    json = request.json()
    try:
        return User.from_json(json)

    except KeyError:
        raise AssertionError(f"Erreur {json['code']}: {json['message']}")
