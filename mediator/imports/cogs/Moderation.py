import disnake as discord
from disnake.ext import commands

class Moderation(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(read_message_history=True,manage_messages=True)
    @commands.slash_command()
    async def wipe(self,itr):
        print(itr.filled_options)
        pass

    @wipe.sub_command()
    async def off(self,itr,count:int=20,ephemeral:bool=False):
        print("off")

def setup(client):
    client.add_cog(Moderation(client))
