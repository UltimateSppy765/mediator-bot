import json

import discord
from discord import app_commands
from discord.ext import commands


class Miscellaneous(commands.Cog):
    """Contains miscellaneous commands."""
    
    def __init__(self, client) -> None:
        self.client = client
        with open("mediator/coglist.json", "r") as file:
            with open(json.load(file)["l10npath"]["Miscellaneous"]) as file2:
                self.l10ndata = json.load(file2)
        
    @app_commands.command(name="ping")
    async def ping(self, itr: discord.Interaction) -> None:
        await itr.response.send_message(f":ping_pong: Bot latency is `{round(self.client.latency * 1000)}ms`", ephemeral=True)
    

async def setup(client) -> None:
    await client.add_cog(Miscellaneous(client))
