
import discord
from discord.ext import commands

class wipe(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_permissions(manage_messages=True)
    @commands.group(invoke_without_command=True)
    async def wipe(self,ctx):
        return await ctx.reply("<:mno:851569517242351616> Missing or Invalid Subcommand.") 
    @wipe.command()
    async def off(self,ctx,count:int=20):
        if count>150 or count<1:
            return await ctx.reply("<:merror:851584410935099423> Please enter a count between 1 and 150.")
        msg=await ctx.reply("<:mwiping:851682672593731596> Wiping Messages...",mention_author=False)
        pur=await ctx.channel.purge(limit=count,before=ctx.message)
        await msg.edit(content=f"<:mwipeyay:851572058382925866> Successfully wiped {len(pur)} message{'s' if len(pur)!=1 else ''}." if len(pur)>0 else "<:mno:851569517242351616> No messages were wiped.")
        return

def setup(client):
    client.add_cog(wipe(client))
