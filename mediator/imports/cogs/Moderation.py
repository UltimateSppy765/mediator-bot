import disnake as discord
from disnake.ext import commands

class Moderation(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(read_message_history=True,manage_messages=True)
    @commands.slash_command()
    async def wipe(self,itr):
        keys=list(itr.options.keys())
        try:
            count=itr.options[keys[0]]['count']
        except KeyError:
            pass
        else:
            if count not in range(1,201):
                return await itr.response.send_message(':x: The message count cannot be less than 1 or more than 200.',ephemeral=True)
            else:
                pass

    @wipe.sub_command()
    async def off(self,itr,count:int=20,ephemeral:bool=False):
        print("off")

def setup(client):
    client.add_cog(Moderation(client))
