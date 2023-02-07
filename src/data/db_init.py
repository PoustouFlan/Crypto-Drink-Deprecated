from tortoise import Tortoise, run_async
from data.models import *

import logging
log = logging.getLogger("CryptoDrink")

async def init():
    await Tortoise.init(
        db_url = 'sqlite://data/db.sqlite3',
        modules = {
            "models": ["data.models"]
        }
    )
    await Tortoise.generate_schemas()

    scoreboard = await Scoreboard.all()
    if len(scoreboard) == 0:
        log.info("Aucun scoreboard n'existe. Création du scoreboard")
        await Scoreboard.create()
        log.info("Scoreboard créé avec succès")
    else:
        log.info("Un scoreboard est déjà existant.")



if __name__ == "__main__":
    run_async(init())
