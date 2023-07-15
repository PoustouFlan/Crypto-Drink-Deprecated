from yaml import safe_load
import discord
from i18n import Translator

configuration_file = open("../configuration.yaml", "r")
configuration = safe_load(configuration_file.read())

TOKEN = configuration['token']
GUILD_ID = configuration['guild_id']
CHANNEL_ID = configuration['channel_id']
LANGUAGE = configuration['locale']
tr = Translator('locales', LANGUAGE)

guild_object = discord.Object(id = GUILD_ID)
