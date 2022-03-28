import asyncio
import json
import os
import traceback

import discord
from discord.ext import commands

activity = discord.Activity(type=discord.ActivityType.watching, name="your messages!")
intents = discord.Intents.default()

with open("mediator/coglist.json", "r") as file:
    cogdata = json.load(file)


# Subclass commands.Bot to allow for stuff like persistent views
class SomeClient(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", activity=activity, intents=intents)
        self.l10nlist = cogdata["l10npath"]

    async def on_ready(self) -> None:
        print(f"Bot is ready.\nLogged in as {str(self.user)} - {self.user}")


client = SomeClient()


async def cog_on_start(client, extension: str) -> str | None:
    try:
        await client.load_extension(extension)
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        return extension


async def main() -> None:
    async with client:
        # Asynchronously loads all extensions and returns a list containing the result values
        results = await asyncio.gather(
            *(
                cog_on_start(client, i["path"])
                for i in cogdata["coglist"]
                if i["load_on_start"]
            )
        )
        # Remove duplicates
        results = list(set(results))
        print(results)
        try:
            results.remove(None)
        except ValueError:
            pass
        reslen = len(results)
        print(
            f"Successfully loaded {reslen} extension{'' if reslen == 1 else 's'}.\nExtensions loaded: {results}"
        )
        await client.start(os.environ["BOT_TOKEN"])


asyncio.run(main())
