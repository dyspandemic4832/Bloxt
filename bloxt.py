import os, sys
import interactions
from interactions import Client, Intents, listen
from interactions.api.events import Component
from interactions.ext import prefixed_commands

from addons.jsonimport import JsonImport

JI = JsonImport("dev_config.json")

bot = Client(
    intents=Intents.DEFAULT | Intents.MESSAGE_CONTENT,
    sync_interactions=True,
    asyncio_debug=True,
    activity=interactions.Activity(
        name="DEBUGGING",
        type=interactions.ActivityType.STREAMING,
        url="https://www.twitch.tv/dyspandemic4832",
    ),
)
prefixed_commands.setup(bot)

@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@listen()
async def on_guild_create(event):
    print(f"guild created : {event.guild.name}")


@listen()
async def on_message_create(event):
    print(f"message received: {event.message.content}")
    

extensions = [
    f"cogs.{f[:-3]}"
    for f in os.listdir("cogs")
    if f.endswith(".py") and not f.startswith("_")
]
for extension in extensions:
    try:
        bot.load_extension(extension)
        print(f"Loaded extension {extension}")
    except interactions.errors.ExtensionLoadException as e:
        print(f"Failed to load extension {extension}.", exc_info=e)

if JI.get_value_from_key("DEBUG") == True and JI.get_value_from_key("DEV_TOKEN") != None:
    bot.start(JI.get_value_from_key("DEV_TOKEN"))
elif JI.get_value_from_key("DEBUG") == False and JI.get_value_from_key("TOKEN") != None:
    bot.start(JI.get_value_from_key("TOKEN"))
else:
    print("Please configure your config file.")