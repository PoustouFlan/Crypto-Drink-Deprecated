from tortoise.models import Model
from tortoise import fields
from datetime import date

import logging
log = logging.getLogger("CryptoDrink")

def strptime(date_str):
    day, month, year = date_str.split()
    month = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
              'Sep', 'Oct', 'Nov', 'Dec'].index(month)
    return date(int(year), month, int(day))

class Challenge(Model):
    id       = fields.UUIDField(pk = True)
    category = fields.CharField(max_length = 255)
    date     = fields.DateField()
    name     = fields.CharField(max_length = 255)
    points   = fields.IntField()
    solves   = fields.SmallIntField()

    @classmethod
    async def get_existing(cls, category, name):
        challenges = await cls.filter(name = name, category = category)
        if len(challenges) == 0:
            return None
        else:
            return challenges[0]

    @classmethod
    async def get_existing_or_create(cls, json):
        category = json['category']
        name = json['name']
        challenge = await Challenge.get_existing(category, name)
        if challenge is None:
            log.info(f"Ajout du challenge : {category}/{name}")
            json_copy = json.copy() # Pour éviter d'altérer le paramètre

            json_copy['date'] = strptime(json['date'])
            return await cls.create(**json_copy)
        else:
            return challenge

    @classmethod
    async def update_existing_or_create(cls, json):
        category = json['category']
        name = json['name']
        json_copy = json.copy() # Pour éviter d'altérer le paramètre
        json_copy['date'] = strptime(json['date'])

        challenge = await Challenge.get_existing(category, name)
        if challenge is None:
            log.info(f"Ajout du challenge : {category}/{name}")
            return await cls.create(**json_copy)
        else:
            log.info(f"Mise à jour du challenge : {category}/{name}")
            challenge = challenge.update_from_dict(json_copy)
            await challenge.save()
            return challenge

    def __str__(self):
        return f"({self.category}/{self.name})"

    def __hash__(self):
        return hash(self.name) ^ hash(self.category)

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

    server_rank       = fields.IntField(default = 2147483647)

    @classmethod
    async def get_existing(cls, username):
        users = await cls.filter(username = username)
        if len(users) == 0:
            return None
        else:
            return users[0]

    @classmethod
    async def get_existing_or_create(cls, json):
        """
        Si un utilisateur du même nom existe, le retourne sans mise à jour.
        Sinon, créée l'utilisateur.
        Les challenges résolus par l'utilisateur ne sont pas mis à jour.
        """
        username = json['username']
        existing_user = await User.get_existing(username)
        if existing_user is None:
            solved_challenges = [
                await Challenge.get_existing_or_create(challenge)
                for challenge in json['solved_challenges']
            ]
            json_copy = json.copy() # Pour éviter d'altérer le paramètre
            del json_copy['solved_challenges']
            json_copy['joined'] = strptime(json['joined'])

            user = await cls.create(**json_copy)
            await user.solved_challenges.add(*solved_challenges)
            return user

        else:
            return existing_user

    @classmethod
    async def update_existing_or_create(cls, json):
        """
        Si un utilisateur du même nom existe, met à jour ses informations
        ainsi que les informations de chacun des challenges qu'il a résolu.
        Sinon, créée l'utilisateur et met à jour les informations des
        challenges résolus.
        """
        username = json['username']
        solved_challenges = [
            await Challenge.get_existing_or_create(challenge)
            for challenge in json['solved_challenges']
        ]
        json_copy = json.copy() # Pour éviter d'altérer le paramètre
        del json_copy['solved_challenges']
        json_copy['joined'] = strptime(json['joined'])

        existing_user = await User.get_existing(username)

        if existing_user is None:
            user = await cls.create(**json_copy)
            await user.solved_challenges.add(*solved_challenges)
            return user

        else:
            existing_user = await existing_user.update_from_dict(json_copy)
            await existing_user.solved_challenges.clear()
            await existing_user.solved_challenges.add(*solved_challenges)
            await existing_user.save()

            return existing_user

    async def new_flags(self, json):
        """
        Met à jour l'utilisateur et renvoie la liste des challenges
        résolus récemment
        """
        solved_challenges = [
            await Challenge.update_existing_or_create(challenge)
            for challenge in json['solved_challenges']
        ]
        actual = set(solved_challenges)
        previous = set(await self.solved_challenges.all())
        diff = actual - previous

        json_copy = json.copy() # Pour éviter d'altérer le paramètre
        del json_copy['solved_challenges']
        json_copy['joined'] = strptime(json['joined'])

        self = await self.update_from_dict(json_copy)
        await self.solved_challenges.clear()
        await self.solved_challenges.add(*solved_challenges)
        await self.save()

        return diff

    def __str__(self):
        return f"{self.username} (#{self.rank})"

class Scoreboard(Model):
    id    = fields.UUIDField(pk = True)
    users = fields.ManyToManyField('models.User')

    async def add_user(self, user: User):
        await self.users.add(user)

    async def add_user_if_not_present(self, user: User):
        users = await self.users.filter(username = user.username)
        if len(users) == 0:
            await self.add_user(user)
            return True
        return False

    async def remove_user_if_present(self, user: User):
        users = await self.users.filter(username = user.username)
        if len(users) == 0:
            return False
        await self.users.remove(*users)
        return True


