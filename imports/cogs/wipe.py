
import discord
from discord.ext import commands

class wipe(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cogs.listener()
    async def on_interaction(self,itr):
        if itr.type==2 and itr.data["name"]=="wipe":
            if itr.data["options"][0]["name"]=="off":
                try:
                    cnt=itr.data["options"][0]["options"][0]["value"]
                except:
                    await wipeoff(itr=itr)
                else:
                    await wipeoff(itr=itr,count=cnt)

    async def wipeoff(itr,count:int=20):
        if count<1 or count>151:
            return await itr.reponse.send_message("<:merror:851584410935099423> Please enter a number between 1 and 150.",ephemeral=True)
        await itr.send_message("This command isn't ready yet.",ephemeral=True)

def setup(client):
    client.add_cog(wipe(client))
