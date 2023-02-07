import discord
import asyncio
from bot_utils import TOKEN
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix = "$ ",
    help_command = None,
    intents = intents
)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")


async def main():
    await bot.start(TOKEN)

asyncio.run(main())
