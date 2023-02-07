from tortoise.models import Model
from tortoise import fields
from datetime import datetime

import logging
log = logging.getLogger("CryptoDrink")

strptime = lambda date: datetime.strptime(date, '%d %b %Y')

class Challenge(Model):
    id       = fields.UUIDField(pk = True)
    category = fields.CharField(max_length = 255)
    date     = fields.DateField()
    name     = fields.CharField(max_length = 255)
    points   = fields.IntField()
    solves   = fields.SmallIntField()

    @classmethod
    async def from_json(cls, json):
        json['date'] = strptime(json['date'])
        challenge = await cls.filter(name = json['name'])
        assert len(challenge) <= 1, (
            "Deux challenges portent le même nom !"
        )
        
        if len(challenge) == 1:
            log.info(f"Le challenge {json['name']} existe déjà.")
            challenge[0] = await challenge[0].update_from_dict(json)
            await challenge[0].save()
            return challenge[0]

        log.info(f"Le challenge {json['name']} n'existe pas.")
        return await cls.create(**json)

    def __str__(self):
        return f"({self.category}/{self.name})"

class User(Model):
    country           = fields.CharField(max_length = 255)
    first_bloods      = fields.SmallIntField()
    joined            = fields.DateField()
    level             = fields.SmallIntField()
    rank              = fields.IntField()
    score             = fields.IntField()
    solved_challenges = fields.ManyToManyField('models.Challenge')
    user_count        = fields.IntField()
    username          = fields.CharField(max_length = 255, pk = True)
    website           = fields.CharField(max_length = 255)

    @classmethod
    async def from_json(cls, json):
        solved_challenges = [
            await Challenge.from_json(challenge)
            for challenge in json['solved_challenges']
        ]
        del json['solved_challenges']
        json['joined'] = strptime(json['joined'])

        user = await cls.filter(username = json['username'])
        assert len(user) <= 1, (
            "Deux utilisateurs ont le même identifiant !"
        )

        if len(user) == 1:
            log.info(f"L'utilisateur {json['username']} existe déjà.")
            user[0] = await user[0].update_from_dict(json)
            await user[0].solved_challenges.clear()
            await user[0].solved_challenges.add(*solved_challenges)
            await user[0].save()
            return user[0]

        log.info(f"L'utilisateur {json['username']} n'existe pas.")

        user = await cls.create(**json)
        await user.solved_challenges.add(*solved_challenges)
        return user

    def __str__(self):
        return f"{self.username} (#{self.rank})"

class Scoreboard(Model):
    users = fields.ManyToManyField('models.User')

    async def add_user(self, user: User):
        await self.users.add(user)
