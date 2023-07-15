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
        description = tr("announce description")
    )
    async def manual_update(self, interaction):
        await interaction.response.defer()
        count = await self.auto_update()
        await interaction.followup.send(
            tr("flags announced", count=count)
        )

    @tasks.loop(minutes = 5)
    async def auto_update(self):
        log.info(tr("auto update log"))
        scoreboards = await Scoreboard.all()
        scoreboard = scoreboards[0]
        users = await scoreboard.users.all()

        counter = 0
        for user in users:
            log.info(tr("updating user log", username=user.username))
            json = get_user(user.username)
            flags = await user.new_flags(json)

            if len(flags) > 0:
                for challenge in flags:
                    counter += 1
                    await self.announce(user, challenge)
        log.info(tr("done"))
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
            title = tr("new flag"),
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
                tr("level", level=user.level) +
                tr("rank", rank=user.rank, count=user.user_count)
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
        flags = tr("ordinal", count=flags)

        if challenge.category in CATEGORY_LINK:
            category_link = CATEGORY_LINK[challenge.category]
            category = f"[{challenge.category}]({category_link})"
        else:
            log.error(tr("category missing", name=challenge.category))
            category = f"{challenge.category}"

        embed.add_field(
            inline = False,
            name = "",
            value = (
                f"**{category}\n**{challenge.name}\n"
                f":star: {challenge.points} ⠀ "
                f":triangular_flag_on_post: {challenge.solves}\n" +
                tr("challenge position", ordinal=flags)
            )
        )

        await channel.send(
            embed = embed,
        )


async def setup(bot):
    await bot.add_cog(Announce(bot), guilds = [guild_object])
