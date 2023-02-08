import discord
from discord.ext import commands
from discord import app_commands
from bot_utils import guild_object

import logging
log = logging.getLogger("CryptoDrink")

from cryptohack import get_user
from data.models import *

class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = "register",
        description = "Inscrit un utilisateur dans le tableau du serveur"
    )
    async def register(self, interaction, user:str):
        try:
            json = get_user(user)
        except AssertionError as e:
            await interaction.response.send_message(str(e))
            return

        user = await User.update_existing_or_create(json)

        scoreboards = await Scoreboard.all()
        scoreboard = scoreboards[0]

        added = await scoreboard.add_user_if_not_present(user)

        if added:
            await interaction.response.send_message(
                f"L'utilisateur {user.username} a été ajouté au tableau.",
            )
        else:
            await interaction.response.send_message(
                f"L'utilisateur {user.username} est déjà présent dans le tableau."
            )

async def setup(bot):
    await bot.add_cog(Register(bot), guilds = [guild_object])
