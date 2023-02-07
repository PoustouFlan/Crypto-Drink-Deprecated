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



if __name__ == "__main__":
    run_async(init())
