import discord,typing
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.Cog.listener()
    async def on_interaction(self,itr):
        if itr.type==2:
            if itr.data["name"]=="wipe":
                return await self.wipeslash(itr)
					
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.group(invoke_without_command=True)
    async def wipe(self,ctx):
        "Base command for wiping messages in a channel."
        return await ctx.reply("<:mno:851569517242351616> Missing or Invalid Subcommand.") 
    @wipe.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(read_message_history=True,send_messages=True,manage_messages=True)
    @commands.guild_only() 
    async def off(self,ctx,count:int=20):
        "Wipes off n messages in a channel with no checks. Maximum 200 messages." 
        if count>200 or count<1:
            return await ctx.reply("<:merror:851584410935099423> Please enter a count between 1 and 200.")
        msg=await ctx.reply("<:mwiping:851682672593731596> Wiping Messages...",mention_author=False)
        pur=await ctx.channel.purge(limit=count,before=ctx.message)
        s='s' if len(pur)!=1 else ''
        await msg.edit(content=f"<:mwipeyay:851572058382925866> Successfully wiped {len(pur)} message{s}." if len(pur)>0 else "<:mno:851569517242351616> No messages were wiped.")
        return
    @wipe.command()
    @commands.bot_has_permissions(read_message_history=True,send_messages=True,manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def user(self,ctx,user:typing.Union[discord.Object,discord.Member],count:int=20):
        "Wipes off messages sent by an individual user."
        return await ctx.reply("Command in Works. :D")
    
    async def wipeslash(self,itr):
        try:
            perms=itr.channel.permissions_for(itr.user).manage_messages
        except:
            return await itr.response.send_message("<:merror:851584410935099423> This command cannot be used in Direct Messages.",ephemeral=True)
        if perms==False:
            return await itr.response.send_message("<:merror:851584410935099423> You cannot use this command.",ephemeral=True)
        if itr.channel.permissions_for(self.user).manage_messages==False or itr.channel.permissions_for(self.user).read_message_history==False:
            if itr.channel.permissions_for(self.user).manage_messages==False and itr.channel.permissions_for(self.user).read_message_history==False:
                missperms="Read Message History\nManage Messages"
            else:
                missperms="Read Message History" if itr.channel.permissions_for(self.user).read_message_history=False else "Manage Messages"
            return await itr.response.send_message(f"<:merror:851584410935099423> I do not have the required permissions to perform this, please check my permissions for this channel:```\n{missperms}\n```",ephemeral=True)
        try:
            count=itr.data["options"][0]["options"][0]["value"]
        except:
            count=20
        if count>200 or count<1:
            return await itr.response.send_message("<:merror:851584410935099423> Please enter a count between 1 and 200.",ephemeral=True)
        if itr.data["options"][0]["name"]=="off":
            await itr.response.defer()
            pur=await itr.channel.purge(limit=count,before=discord.Object(itr.id))
            s='s' if len(pur)!=1 else ''
        return await itr.followup.send(content=f"<:mwipeyay:851572058382925866> Successfully wiped {len(pur)} message{s}." if len(pur)>0 else "<:mno:851569517242351616> No messages were wiped.")
        
def setup(client):
    client.add_cog(Moderation(client))
