import discord
from discord.ext import commands
from discord import app_commands
from bot_utils import guild_object

import logging
log = logging.getLogger("CryptoDrink")

from cryptohack import get_user, CATEGORY_LINK
from data.models import *

from babel.dates import format_date
import matplotlib.pyplot as plt


def create_plot(challenges, filename):
    try:
        dates = [chal.date for chal in challenges[::-1]]
        score = 0
        scores = []
        for chal in challenges[::-1]:
            score += chal.points
            scores.append(score)

        plt.plot(dates, scores, color='gold')
        plt.xticks(color='white')
        plt.yticks(color='white')
        plt.gca().spines['bottom'].set_color('white')
        plt.gca().spines['left'].set_color('white')
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.xticks(rotation=45)
        plt.tick_params(axis='x',colors='white')
        plt.tick_params(axis='y',colors='white')
        plt.tight_layout()

        plt.savefig(filename, dpi=300, transparent=True)
        plt.close()
    except Exception as e:
        log.exception(str(e))

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
        try:
            json = get_user(user)
        except AssertionError as e:
            await interaction.response.send_message(str(e))
            return

        user = await User.get_existing_or_create(json)
        flags = await user.new_flags(json)

        if len(flags) > 0:
            scoreboards = await Scoreboard.all()
            scoreboard = scoreboards[0]

            users = await scoreboard.users.filter(username = user.username)
            if len(users) > 0:
                announce = self.bot.get_cog("Announce")
                for challenge in flags:
                    await announce.announce(user, challenge)

        embed = discord.Embed(
            title = f"Profil de {user.username}",
            colour = discord.Colour.orange()
        )

        if user.country == '':
            pays = ":globe_with_meridians:"
        else:
            pays = f":flag_{user.country}:"
        if user.website == '':
            website = ''
        else:
            website = f"[Site web]({user.website})\n"

        embed.add_field(
            inline = False,
            name = "Informations personnelles",
            value = (
                f"{pays} [{user.username}](https://cryptohack.org/user/{user.username})\n"
                f"CryptoHacker depuis le {format_date(user.joined, locale='fr')}\n"
                f"{website}"
            )
        )

        value = ""
        challenges = await user.solved_challenges.all()
        for chal in challenges[:5]:
            if chal.category in CATEGORY_LINK:
                category_link = CATEGORY_LINK[chal.category]
                challenge = f"[{chal.category}]({category_link})"
            else:
                log.error(f"{chal.category} absent de la liste des catégories !")
                challenge = f"{chal.category}"
            value += f":star: {chal.points} | {challenge}/{chal.name}\n"

        filename = f"tmp/{user.username}_plot.png"
        create_plot(challenges, filename)
        file = discord.File(filename, filename = filename[4:])
        embed.set_image(url = f"attachment://{filename[4:]}")

        embed.add_field(
            name = "Statistiques",
            inline = False,
            value = (
                f":star: {user.score} ⠀ "
                f":triangular_flag_on_post: {len(challenges)}\n" +
                (":drop_of_blood:" * user.first_bloods) +
                ("\n" * (user.first_bloods > 0)) +
                f"Niveau : {user.level}\n"
                f"Rang : #{user.rank} / {user.user_count}\n"
            )
        )

        embed.add_field(
            inline = False,
            name = "Derniers challenges résolus",
            value = value
        )

        await interaction.response.send_message(
            "",
            file = file,
            embed = embed,
        )

async def setup(bot):
    await bot.add_cog(UserInfo(bot), guilds = [guild_object])
