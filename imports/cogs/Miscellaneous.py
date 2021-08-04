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
                await toxicchk(itr=itr)
    
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
        if score>=80:
            text=f"||{text}||"
        desc=f"**Text you input:** {text}\n__Toxicity Score:__```\n{score}%\n```"
        embed=discord.Embed(title=":test_tube: Toxicity Check",description=desc,colour=3092791)
        return await itr.edit_original_message(embed=embed)

def setup(client):
    client.add_cog(Miscellaneous(client))
