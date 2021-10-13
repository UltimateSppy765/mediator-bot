import disnake as discord
from disnake.ext import commands

class Moderation(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.has_permissions(manage_messages=True)
    @commands.slash_command()
    async def wipe(self,itr):
        pass

def setup(client):
    client.add_cog(Moderation(client))
