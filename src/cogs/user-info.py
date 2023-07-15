import discord
from discord.ext import commands
from discord import app_commands
from bot_utils import *

import logging
log = logging.getLogger("CryptoDrink")

from cryptohack import get_user, CATEGORY_LINK, ALL_CHALLENGES
from data.models import *

from babel.dates import format_date
import matplotlib.pyplot as plt
from collections import defaultdict


def create_plot(challenges, filename):
    dates = []
    score = 0
    scores = []
    for chal in challenges[::-1]:
        dates.append(chal.date)
        scores.append(score)
        score += chal.points
        dates.append(chal.date)
        scores.append(score)

    plt.grid(which='major', axis='y', color='gray', linestyle='dashed', linewidth=0.5, alpha=0.5)
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

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = "user-info",
        description = tr("userinfo description")
    )
    async def user_info(self, interaction, user:str):
        try:
            json = get_user(user)
        except AssertionError as e:
            await interaction.response.send_message(str(e))
            return

        await interaction.response.defer()

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
            title = tr("profile header", username=user.username),
            colour = discord.Colour.orange()
        )

        if user.country == '':
            pays = ":globe_with_meridians:"
        else:
            pays = f":flag_{user.country}:"
        if user.website == '':
            website = ''
        else:
            website = tr("website", url=user.website)

        embed.add_field(
            inline = False,
            name = tr("personal information"),
            value = (
                f"{pays} [{user.username}](https://cryptohack.org/user/{user.username})\n" +
                tr("cryptohacker since", date=user.joined) +
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
                log.error(tr("category missing", name=chal.category))
                challenge = f"{chal.category}"
            value += f":star: {chal.points} | {challenge}/{chal.name}\n"

        filename = f"tmp/{user.username}_plot.png"
        create_plot(challenges, filename)
        file = discord.File(filename, filename = filename[4:])
        embed.set_image(url = f"attachment://{filename[4:]}")

        embed.add_field(
            name = tr("stats"),
            inline = False,
            value = (
                f":star: {user.score} ⠀ "
                f":triangular_flag_on_post: {len(challenges)}\n" +
                (":drop_of_blood:" * user.first_bloods) +
                ("\n" * (user.first_bloods > 0)) +
                tr("level", level=user.level) +
                tr("rank", rank=user.rank, count=user.user_count)
            )
        )

        embed.add_field(
            inline = False,
            name = tr("last solves"),
            value = value
        )

        categories = defaultdict(lambda: 0)
        for chal in challenges:
            categories[chal.category] += 1
        value = ""
        for category in ALL_CHALLENGES:
            solved = categories[category]
            total = len(ALL_CHALLENGES[category])
            bars = 10 * solved // total
            bar = "▰"*bars + "▱"*(10 - bars)
            star = ":star2:" if solved == total else ":black_large_square:"
            value += f"{star} {bar} {category}: {solved} / {total}\n"

        embed.add_field(
            inline = False,
            name = tr("categories"),
            value = value
        )

        await interaction.followup.send(
            "",
            file = file,
            embed = embed,
        )

async def setup(bot):
    await bot.add_cog(UserInfo(bot), guilds = [guild_object])
