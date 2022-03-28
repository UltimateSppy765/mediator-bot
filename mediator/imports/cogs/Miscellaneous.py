import discord
from discord import app_commands
from discord.ext import commands


class Miscellaneous(commands.Cog):
    """Contains miscellaneous commands."""
    
    def __init__(self, client) -> None:
        self.client = client
        
    @app_commands.command(name="ping")
    async def ping(self, itr: discord.Interaction) -> None:
        await itr.response.send_message(f":ping_pong: Bot latency is `{round(self.client.latency * 1000)}ms`", ephemeral=True)
    

async def setup(client) -> None:
    await client.add_cog(Miscellaneous(client))
