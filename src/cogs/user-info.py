import discord
from discord.ext import commands
from discord import app_commands
from bot_utils import guild

import logging
log = logging.getLogger("CryptoDrink")

from cryptohack import get_user
from data.models import *

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sync(self, ctx):
        log.info("Syncing...")
        fmt = await ctx.bot.tree.sync(guild = ctx.guild)
        s = "" if len(fmt) < 2 else "s"
        log.info("Sync complete")
        await ctx.send(f"{len(fmt)} commande{s} synchronisée{s}.")

    @app_commands.command(
        name = "user-info",
        description = "Affiche les informations concernant un utilisateur"
    )
    async def user_info(self, interaction, user:str):
        json = get_user(user)
        user = await User.from_json(json)
        log.info(user)
        await interaction.response.send_message(
            "pong", ephemeral = True
        )

async def setup(bot):
    await bot.add_cog(UserInfo(bot), guilds = [guild])
