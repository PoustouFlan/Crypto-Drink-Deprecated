import discord
from discord.ext import commands
from discord import app_commands
from bot_utils import guild_object

import logging
log = logging.getLogger("CryptoDrink")

from cryptohack import get_user
from data.models import *

class Unregister(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = "unregister",
        description = "Désinscrit un utilisateur du tableau du serveur"
    )
    async def unregister(self, interaction, user:str):
        try:
            json = get_user(user)
        except AssertionError as e:
            await interaction.response.send_message(str(e))
            return

        user = await User.update_existing_or_create(json)

        scoreboards = await Scoreboard.all()
        scoreboard = scoreboards[0]

        removed = await scoreboard.remove_user_if_present(user)

        if removed:
            await interaction.response.send_message(
                f"L'utilisateur {user.username} a été supprimé du tableau.",
            )
        else:
            await interaction.response.send_message(
                f"L'utilisateur {user.username} n'est pas présent dans le tableau."
            )

async def setup(bot):
    await bot.add_cog(Unregister(bot), guilds = [guild_object])
