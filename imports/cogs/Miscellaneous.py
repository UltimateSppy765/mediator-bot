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
            elif itr.data["name"]=="toxicitycheck":
                await self.toxicchk(ir=itr)
    
    @commands.command()
    async def ping(self,ctx):
        "Shows bot latency."
        await ctx.reply(f"Bot ping is `{round(self.client.latency*1000)}ms`.",mention_author=False)

    async def toxicchk(ir):
        try:
            for k in [0,1]:
                if ir.data["options"][i]["name"]=="hidden":
                    hd=ir.data["options"][i]["value"]
        except:
            hd=False
        await ir.response.defer(ephemeral=hd)
        for i in [0,1]:
            if ir.data["options"][i]["name"]=="text":
                text=ir.data["options"][i]["value"]
        score=getscore(text)
        if score>=80:
            text=f"||{text}||"
        desc=f"**Text you input:** {text}\n__Toxicity Score:__```\n{score}%\n```"
        embed1=discord.Embed(title=":test_tube: Toxicity Check",description=desc,colour=3092791)
        return await ir.edit_original_message(embed=embed1)

def setup(client):
    client.add_cog(Miscellaneous(client))
