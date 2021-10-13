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

    @commands.slash_command()
    async def toxicitycheck(self,itr,text:str,hidden:bool=True):
        await itr.response.defer(ephemeral=hidden)
        text=text.strip()
        score=getscore(text)
        if score>=80:
            text=f"||{text}||"
        desc=f"**Text you input:** {text}\n__Toxicity Score:__```\n{score}%\n```"
        if score==50:
            desc=desc+"**__Note:__** The API might've failed to determine a value for the given text, so it's toxicity percentage is set to `50%`" 
        embed1=discord.Embed(title=":test_tube: Toxicity Check",description=desc,colour=3092791)
        return await itr.edit_original_message(embed=embed1)

def setup(client):
    client.add_cog(Miscellaneous(client))
