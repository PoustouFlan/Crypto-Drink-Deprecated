import discord
from discord.ext import commands
from discord import app_commands
from bot_utils import guild_object

import logging
log = logging.getLogger("CryptoDrink")

from data.models import *

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = "scoreboard",
        description = "Affiche le tableau des scores du serveur"
    )
    async def scoreboard(self, interaction):
        await interaction.response.defer()
        
        scoreboards = await Scoreboard.all()
        scoreboard = scoreboards[0]
        users = await scoreboard.users.all()

        users.sort(
            key = lambda user: user.score,
            reverse = True
        )

        embed = discord.Embed(
            # title = f"Tableau des scores",
            colour = discord.Colour.blue()
        )

        digits = len(str(len(users)))

        for page in range((len(users) // 5) + 1):
            leaderboard = ""
            for i, user in enumerate(users[5*page:5*page + 5]):
                if user.country == '':
                    pays = ":globe_with_meridians:"
                else:
                    pays = f":flag_{user.country}:"

                old_place = user.server_rank
                new_place = i + 1 + 5 * page
                user.server_rank = new_place
                challenges = await user.solved_challenges.all()
                await user.save()
                if new_place < old_place:
                    emote = ":arrow_up_small:"
                elif new_place == old_place:
                    emote = ":black_large_square:"
                else:
                    emote = ":arrow_down_small:"

                score = str(user.score).ljust(5)
                flags = str(len(challenges)).ljust(3)

                leaderboard += (
                    f"{emote} `{str(new_place).rjust(digits)}` | "
                    f":star: `{score}` ⠀ "
                    f":triangular_flag_on_post: `{flags}` | "
                    f"{pays} [{user.username}](https://cryptohack.org/user/{user.username})\n"
                )

            if page == 0:
                name = "Tableau des scores"
            else:
                name = ""

            embed.add_field(
                inline = False,
                name = name,
                value = leaderboard
            )

        await interaction.followup.send(
            "",
            embed = embed,
        )

async def setup(bot):
    await bot.add_cog(Leaderboard(bot), guilds = [guild_object])
