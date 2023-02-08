import discord
from discord.ext import commands
from discord import app_commands
from bot_utils import *

from cryptohack import CATEGORY_LINK

import logging
log = logging.getLogger("CryptoDrink")

class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def announce(self, user, challenge):

        guild = self.bot.get_guild(GUILD_ID)
        channel = await guild.fetch_channel(CHANNEL_ID)

        if user.country == '':
            pays = ":globe_with_meridians:"
        else:
            pays = f":flag_{user.country}:"
        challenges = await user.solved_challenges.all()

        embed = discord.Embed(
            title = "Nouveau flag !",
            colour = discord.Colour.red()
        )

        embed.add_field(
            inline = False,
            name = "Flagger",
            value = (
                f"{pays} [{user.username}](https://cryptohack.org/user/{user.username})\n"
                f":star: {user.score} ⠀ "
                f":triangular_flag_on_post: {len(challenges)}\n" +
                (":drop_of_blood:" * user.first_bloods) +
                f"Niveau : {user.level}\n"
                f"Rang : #{user.rank} / {user.user_count}\n"
            )
        )

        if challenge.category in CATEGORY_LINK:
            category_link = CATEGORY_LINK[challenge.category]
            category = f"[{challenge.category}]({category_link})"
        else:
            log.error(f"{challenge.category} absent de la liste des catégories !")
            category = f"{challenge.category}"

        embed.add_field(
            inline = False,
            name = "",
            value = (
                f"**{category}\n**{challenge.name}\n"
                f":star: {challenge.points} ⠀ "
                f":triangular_flag_on_post: {challenge.solves}\n"
            )
        )

        await channel.send(
            embed = embed,
        )


async def setup(bot):
    await bot.add_cog(Announce(bot), guilds = [guild_object])
