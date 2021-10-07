import disnake as discord
from disnake.ext import commands
from imports.modules.perspective import getscore

class Miscellaneous(commands.Cog):
    """Miscellaneous commands."""
    def __init__(self,client):
        self.client=client

    @commands.slash_command()
    async def ping(self,itr):
        """Shows bot ping/latency."""
        await itr.response.send_message(f'Bot latency is `{round(self.client.latency*1000)}ms`.',ephemeral=True)

def setup(client):
    client.add_cog(Miscellaneous(client))
