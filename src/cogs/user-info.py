import discord
from discord.ext import commands
from discord import app_commands
from bot_utils import guild

import logging
log = logging.getLogger("CryptoDrink")

from cryptohack import get_user
from data.models import *


import locale

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

        embed = discord.Embed()

        if user.country == '':
            pays = ":globe_with_meridians:"
        else:
            pays = f":flag_{user.country}:"
        if user.website == '':
            website = ''
        else:
            website = f"[Site web]({user.website})\n"

        locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')

        embed.add_field(
            inline = False,
            name = "Informations personnelles",
            value = (
                f"{pays} [{user.username}](https://cryptohack.org/user/{user.username})\n"
                f"CryptoHacker depuis le {user.joined.strftime('%d %b %Y')}\n"
                f"{website}"
            )
        )
        embed.add_field(
            name = "Statistiques",
            inline = False,
            value = (
                f":star: {user.score}\n" +
                (":drop_of_blood:" * user.first_bloods) +
                ("\n" * (user.first_bloods > 0)) +
                f"Niveau : {user.level}\n"
                f"Rang : #{user.rank} / {user.user_count}\n"
            )
        )

        value = ""
        challenges = await user.solved_challenges.all()
        for chal in challenges[:5]:
            value += f":star: {chal.points} | {chal.category}/{chal.name}\n"
        embed.add_field(
            inline = False,
            name = "Derniers challenges résolus",
            value = value
        )

        # Liste des derniers challenges résolus ?

        await interaction.response.send_message(
            f"Voici les informations concernant {user.username}",
            embed = embed,
        )

async def setup(bot):
    await bot.add_cog(UserInfo(bot), guilds = [guild])
