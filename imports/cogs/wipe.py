
import discord
from discord.ext import commands

class wipe(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    

def setup(client):
    client.add_cog(wipe(client))
