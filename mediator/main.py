import asyncio
import json
import os

import discord
from discord.ext import commands

activity = discord.Activity(type=discord.ActivityType.watching, name="your messages!")
intents = discord.Intents.default()


class SomeClient(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", activity=activity, intents=intents)

    async def on_ready(self) -> None:
        print(f"Bot is ready.\nLogged in as {str(self.user)} - {self.user}")


client = SomeClient()

with open("mediator/coglist.json", "r") as file:
    cogdata = json.load(file)

async def main() -> None:
    async with client:
        await asyncio.gather(*(client.load_extension(i) for i in cogdata["coglist"] if i["load_on_start"]))
        await client.start(os.environ["BOT_TOKEN"])


asyncio.run(main())
