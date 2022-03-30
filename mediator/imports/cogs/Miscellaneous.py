import json

import aiofiles
import discord
from discord import app_commands
from discord.ext import commands


class Miscellaneous(commands.Cog):
    """Contains miscellaneous commands."""
    
    @classmethod
    async def create(cls, client):
        self = Miscellaneous(client)
        async with aiofiles.open(client.l10nlist["Miscellaneous"], "r") as file:
            self.l10ndata = json.loads(await file.read())
        return self
    
    #def __init__(self, client) -> None:
        #self.client = client
        #with open(client.l10nlist["Miscellaneous"], "r") as file:
            #self.l10ndata = json.load(file)

    @app_commands.command(name="ping")
    async def ping(self, itr: discord.Interaction) -> None:
        await itr.response.send_message(
            self.l10ndata["ping"]["response"][str(itr.locale)].format(
                round(self.client.latency * 1000)
            ),
            ephemeral=True,
        )


async def setup(client) -> None:
    cog = await Miscellaneous.create(client)
    await client.add_cog(cog)
    #await client.add_cog(Miscellaneous(client))
