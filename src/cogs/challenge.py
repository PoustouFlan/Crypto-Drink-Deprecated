import discord
from discord.ext import commands, tasks
from discord import app_commands
from bot_utils import *

from cryptohack import get_user, CATEGORY_LINK
from data.models import *

import logging
log = logging.getLogger("CryptoDrink")

class Select(discord.ui.Select):
    def __init__(self, challenges, interaction, category):
        self.interaction = interaction
        self.category = category
        self.challenges = challenges
        self.answer = None
        options = [
            discord.SelectOption(label=challenge.name) for challenge in challenges
        ]
        placeholder = "Sélectionnez le challenge désiré"
        super().__init__(
            placeholder = placeholder,
            max_values = 1,
            min_values = 1,
            options = options
        )

    async def callback(self, interaction):
        response = await self.interaction.original_response()
        name = self.values[0]
        for challenge in self.challenges:
            if challenge.name == name:
                break

        await Flaggers.display_challenge(interaction, challenge)


class SelectView(discord.ui.View):
    def __init__(self, challenges, interaction, category):
        super().__init__()
        self.add_item(Select(challenges, interaction, category))

class Flaggers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = "challenge",
        description = "Affiche les flaggers d'un challenge dans le serveur"
    )
    async def challenge(self, interaction, category: str, name: str = ""):

        if name == "":
            challenges = await Challenge.filter(
                category = category
            )
            if len(challenges) == 0:
                await interaction.response.send_message(
                    "Cette catégorie n'est pas présente dans la base de données."
                )
                return

            view = SelectView(challenges, interaction, category)

            await interaction.response.send_message(
                "Sélectionnez le challenge désiré.",
                view = view,
                ephemeral = True
            )

        else:
            challenges = await Challenge.filter(
                name = name,
                category = category
            )
            if len(challenges) == 0:
                await interaction.response.send_message(
                    "Ce challenge n'est pas présent dans la base de données."
                )
                return
            challenge = challenges[0]

            await Flaggers.display_challenge(interaction, challenge)

    @staticmethod
    async def display_challenge(interaction, challenge):
        scoreboards = await Scoreboard.all()
        scoreboard = scoreboards[0]
        users = await scoreboard.users.all()

        embed = discord.Embed(
            #title = "Nouveau flag !",
            colour = discord.Colour.red()
        )

        if challenge.category in CATEGORY_LINK:
            category_link = CATEGORY_LINK[challenge.category]
            category = f"[{challenge.category}]({category_link})"
        else:
            log.error(f"{challenge.category} absent de la liste des catégories !")
            category = f"{challenge.category}"

        flags = 0
        value = ""
        for user in users:
            if user.country == '':
                pays = ":globe_with_meridians:"
            else:
                pays = f":flag_{user.country}:"

            challenges = await user.solved_challenges.filter(
                name = challenge.name,
                category = challenge.category
            )
            if len(challenges) > 0:
                value += (
                    f"{pays} [{user.username}](https://cryptohack.org/user/{user.username})\n"
                )
                flags += 1

        embed.add_field(
            inline = False,
            name = "",
            value = (
                f"**{category}\n**{challenge.name}\n"
                f":star: {challenge.points} ⠀ "
                f":triangular_flag_on_post: {challenge.solves}\n"
                f"{flags} :triangular_flag_on_post: dans le scoreboard\n"
            )
        )

        embed.add_field(
            inline = False,
            name = "Flaggers",
            value = value,
        )

        await interaction.response.send_message(
            "",
            embed = embed,
        )

async def setup(bot):
    await bot.add_cog(Flaggers(bot), guilds = [guild_object])
