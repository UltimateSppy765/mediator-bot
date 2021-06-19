import discord,typing
from discord.ext import commands

class wipe(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_interaction(self,itr):
        if itr.type==discord.InteractionType.application_command and itr.data["name"]=="wipe":
            if itr.data["options"][0]["name"]=="off":
                try:
                    perms=itr.channel.permissions_for(itr.user).manage_messages
                except:
                    return await itr.response.send_message("<:merror:851584410935099423> This command cannot be used in Direct Messages.",ephemeral=True)
                if perms:
                    pass
                else:
                    return await itr.response.send_message("<:merror:851584410935099423> You cannot use this command.",ephemeral=True)
                try:
                    count=itr.data["options"][0]["options"][0]["value"]
                except:
                    count=20
                if count>200 or count<1:
                    return await itr.response.send_message("<:merror:851584410935099423> Please enter a count between 1 and 200.",ephemeral=True)
                await itr.response.defer()
                pur=await itr.channel.purge(limit=count,before=discord.Object(itr.id))
                s='s' if len(pur)!=1 else ''
                await itr.edit_message(f"<:mwipeyay:851572058382925866> Successfully wiped {len(pur)} message{s}." if len(pur)>0 else "<:mno:851569517242351616> No messages were wiped.")
                return
					
    @commands.has_permissions(manage_messages=True)
    @commands.group(invoke_without_command=True)
    async def wipe(self,ctx):
        "Base command for wiping messages in a channel."
        return await ctx.reply("<:mno:851569517242351616> Missing or Invalid Subcommand.") 
    @wipe.command()
    async def off(self,ctx,count:int=20):
        "Wipes off n messages in a channel with no checks. Maximum 200 messages." 
        if count>200 or count<1:
            return await ctx.reply("<:merror:851584410935099423> Please enter a count between 1 and 200.")
        msg=await ctx.reply("<:mwiping:851682672593731596> Wiping Messages...",mention_author=False)
        pur=await ctx.channel.purge(limit=count,before=ctx.message)
        s='s' if len(pur)!=1 else ''
        await msg.edit(content=f"<:mwipeyay:851572058382925866> Successfully wiped {len(pur)} message{s}." if len(pur)>0 else "<:mno:851569517242351616> No messages were wiped.")
        return
    #@wipe.command()
    #async def user(self,ctx,user:typing.Union[discord.Snowflake,discord.Member],count:int=20):
        #"Wipes off messages sent by an individual user."
        #return await ctx.reply("Command in Works. :D")

def setup(client):
    client.add_cog(wipe(client))
