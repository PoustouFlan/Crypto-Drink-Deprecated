import discord
from discord.ext import commands, tasks
from discord import app_commands
from bot_utils import *

from cryptohack import get_user, CATEGORY_LINK
from data.models import *

import logging
log = logging.getLogger("CryptoDrink")

class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_update.start()

    @app_commands.command(
        name = "update",
        description = "Annonce les flags récents des membres du tableau"
    )
    async def manual_update(self, interaction):
        try:
            await interaction.response.defer()
            counter = await self.auto_update()
            s = "" if counter < 2 else "s"
            ont = "a" if counter < 2 else "ont"
            await interaction.followup.send(
                f"{counter} flag{s} récent{s} {ont} été annoncé{s}."
            )
        except Exception as e:
            log.error(e)

    @tasks.loop(minutes = 5)
    async def auto_update(self):
        log.info("Updating scores")
        scoreboards = await Scoreboard.all()
        scoreboard = scoreboards[0]
        users = await scoreboard.users.all()

        counter = 0
        for user in users:
            log.info(f"  - Updating {user.username}")
            json = get_user(user.username)
            flags = await user.new_flags(json)

            if len(flags) > 0:
                for challenge in flags:
                    counter += 1
                    await self.announce(user, challenge)
        log.info("Done")
        return counter


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

        scoreboards = await Scoreboard.all()
        scoreboard = scoreboards[0]
        users = await scoreboard.users.all()
        flags = 0
        for user in users:
            challenges = await user.solved_challenges.filter(
                name = challenge.name,
                category = challenge.category
            )
            if len(challenges) > 0:
                flags += 1
        flags = "1er" if flags == 1 else f"{flags}e"

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
                f"{flags} :triangular_flag_on_post: du scoreboard\n"
            )
        )

        await channel.send(
            embed = embed,
        )


async def setup(bot):
    await bot.add_cog(Announce(bot), guilds = [guild_object])
