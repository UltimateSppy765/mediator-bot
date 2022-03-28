import asyncio
import json
import os
import traceback

import discord
from discord.ext import commands

activity = discord.Activity(type=discord.ActivityType.watching, name="your messages!")
intents = discord.Intents.default()


class SomeClient(commands.Bot): # Subclass commands.Bot to allow for stuff like persistent views
    def __init__(self) -> None:
        super().__init__(command_prefix="!", activity=activity, intents=intents)

    async def on_ready(self) -> None:
        print(f"Bot is ready.\nLogged in as {str(self.user)} - {self.user}")


client = SomeClient()

with open("mediator/coglist.json", "r") as file:
    cogdata = json.load(file)

async def cog_on_start(client, extension: str) -> str | None:
    try:
        await client.load_extension(extension)
    except:
        print(traceback.format_exc())
        return None
    else:
        return extension

async def main() -> None:
    async with client:
        loadedcogs = await asyncio.gather(*(cog_on_start(client, i["path"]) for i in cogdata["coglist"] if i["load_on_start"])) # Asynchronously loads all extensions and returns a list containing the result values
        loadedcogs = list(set(loadedcogs)) # Removes duplicates
        loadedcogs.remove(None) # A None will always be there
        print(f"Successfully loaded {len(loadedcogs)} extension{'' if len(loadedcogs) == 1 else 's'}.\nExtensions loaded: {loadedcogs}")
        await client.start(os.environ["BOT_TOKEN"])


asyncio.run(main())
