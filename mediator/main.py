import asyncio
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


async def main() -> None:
    async with client:
        await client.start(os.environ["BOT_TOKEN"])


asyncio.run(main())
