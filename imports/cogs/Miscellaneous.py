import discord
from discord.ext import commands
from imports.modules.perspective import getscore

class Miscellaneous(commands.Cog):
    def __init__(self,client):
        self.client=client
    
    @commands.Cog.listener()
    async def on_interaction(self,itr):
        if itr.type==discord.InteractionType.application_command:
            if itr.data["name"]=="ping":
                await itr.response.send_message(f"Bot ping is `{round(self.client.latency*1000)}ms`.",ephemeral=True)
    
    @commands.command()
    async def ping(self,ctx):
        "Shows bot latency."
        await ctx.reply(f"Bot ping is `{round(self.client.latency*1000)}ms`.",mention_author=False)

    async def toxicchk(itr):
        try:
            for k in [0,1]:
                if itr.data["options"][i]["name"]=="hidden":
                    hd=itr.data["options"][i]["value"]
        except:
            hd=False
        await itr.response.defer(ephemeral=hd)
        for i in [0,1]:
            if itr.data["options"][i]["name"]=="text":
                text=itr.data["options"][i]["value"]
        score=getscore(text)
        

def setup(client):
    client.add_cog(Miscellaneous(client))
