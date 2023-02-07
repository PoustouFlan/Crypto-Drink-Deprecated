import discord
import asyncio
from bot_utils import TOKEN
from discord.ext import commands

import logging
log = logging.getLogger("CryptoDrink")
log.setLevel(logging.DEBUG)
stream = logging.StreamHandler()
log.addHandler(stream)

from data.db_init import init
from data.models import *

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix = "$ ",
    help_command = None,
    intents = intents
)

initial_extensions = [
    "cogs.user-info",
]


@bot.event
async def on_ready():
    log.info(f"Connecté en tant que {bot.user}")
    # await bot.tree.sync(guild = guild)

async def load():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            log.info(f"{extension} chargée avec succès")
        except Exception as e:
            log.error(f"Échec du chargement de {extension}")
            log.error(e)


async def main():
    await init()
    await load()

    scoreboard = await Scoreboard.all()
    if len(scoreboard) == 0:
        log.info("Aucun scoreboard n'existe. Création du scoreboard")
        await Scoreboard.create()
        log.info("Scoreboard créé avec succès")
    else:
        log.info("Un scoreboard est déjà existant.")

    await bot.start(TOKEN)

asyncio.run(main())
