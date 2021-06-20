import discord
from discord.ext import commands

class Miscellaneous(commands.Cog):
    def __init__(self,client):
        self.client=client
    
    @commands.Cog.listener()
    async def on_interaction(self,itr):
        if itr.type==2:
            if itr.data["name"]=="ping":
                await self.pingslash(itr)
    
    @commands.command()
    async def ping(self,ctx):
        "Shows bot latency."
        await ctx.reply(f"Bot ping is `{round(self.client.latency*1000)}ms`.",mention_author=False)
    
    async def pingslash(self,itr):
        await itr.response.send_message(f"Bot ping is `{round(self.client.latency*1000)}ms`.",ephemeral=True)

def setup(client):
    client.add_cog(Miscellaneous(client))
