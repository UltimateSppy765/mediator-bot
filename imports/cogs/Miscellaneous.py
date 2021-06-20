import discord
from discord.ext import commands

class Miscellaneous(commands.Cog):
    def __init__(self,client):
        self.client=client
    
    @commands.command()
    async def ping(self,ctx):
        "Shows bot latency."
        await ctx.reply(f"Bot ping is `{round(self.client.latency*1000)}ms`.",mention_author=False)

def setup(client):
    client.add_cog(Miscellaneous(client))
