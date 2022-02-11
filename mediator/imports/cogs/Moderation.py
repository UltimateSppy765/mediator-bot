import os,durations,requests,calendar
import disnake as discord
from datetime import datetime,timedelta,timezone
from disnake.ext import commands

class WipeChecks():
    def __init__(self,count:int,user_id:int=None,text:str=None):
        self.counter=1
        self.count=count
        self.user_id=user_id
        self.textchk=text
    
    def usercheck(self,m):
        if self.counter>self.count:
            return False
        if m.author.id==self.user_id:
            self.counter+=1
            return True

    def hastextcheck(self,m):
        if self.counter>self.count:
            return False
        if self.textchk in m.content.lower():
            if self.user_id:
                if self.user_id==m.author.id:
                    self.counter+=1
                    return True
                else:
                    return False
            else:
                self.counter+=1
                return True
        else:
            return False

class Wipedone(discord.ui.View):
    def __init__(self,followup,message):
        self.responded=False
        self.followup=followup
        self.message=message
        super().__init__(timeout=5)

    @discord.ui.button(label="Got it!",style=discord.ButtonStyle.green)
    async def wipegotit(self,btn:discord.ui.Button,itr:discord.MessageInteraction):
        if itr.user.id!=itr.message.interaction.user.id:
            return await itr.response.send_message(':x: You cannot use a button on a command invoked by someone else.',ephemeral=True)
        self.responded=True
        await self.followup.delete_message(itr.message.id)

    async def on_timeout(self):
        if not self.responded:
            return await self.message.edit(view=None)

class Moderation(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.bot_has_permissions(read_message_history=True,manage_messages=True)
    @commands.has_permissions(manage_messages=True,read_message_history=True)
    @commands.slash_command()
    async def wipe(self,itr):
        pass

    @wipe.error
    async def wipe_error(self,itr,error):
        if isinstance(error,commands.MissingPermissions):
            return await itr.response.send_message(':x: You need to have the `Manage Messages` and `Read Message History` permissions in this channel to use this command.',ephemeral=True)
        elif isinstance(error,commands.BotMissingPermissions):
            strr=''
            for i in error.missing_permissions:
                i=i.replace('_',' ')
                i=i.title()
                strr=strr+f'• {i}\n'
            return await itr.response.send_message(f':x: The bot does not have the following permissions in this channel to run this command:```\n{strr}```',ephemeral=True)
        elif isinstance(error,discord.HTTPException):
            if isinstance(error,discord.Forbidden):
                text=f':x: The bot is forbidden to perform some actions involved in this command. ```\n{error.text}\n```'
            else:
                text=f':x: The bot ran into an error while trying to execute this command. ```\n{error.text}\n```'
            if itr.response.is_done():
                return await itr.edit_original_message(text)
            else:
                return await itr.response.send_message(text,ephemeral=True)

    @wipe.sub_command()
    async def off(self,itr,count:int=20,hidden:bool=False):
        await itr.response.defer(ephemeral=hidden)
        pur=await itr.channel.purge(limit=count,before=itr,after=datetime.now()-timedelta(days=14),bulk=True,oldest_first=False)
        await itr.edit_original_message(content=f":broom: Successfully wiped {len(pur)} message{'s' if len(pur)>1 else ''}." if len(pur)>0 else ":negative_squared_cross_mark: No messages were wiped.",view=Wipedone(followup=itr.followup,message=await itr.original_message()) if not hidden else None)

    @wipe.sub_command()
    async def user(self,itr,user:discord.User,count:int=20,hidden:bool=False):
        await itr.response.defer(ephemeral=hidden)
        twe=datetime.now()-timedelta(days=14)
        pur=await itr.channel.purge(check=WipeChecks(count=count,user_id=user.id).usercheck,limit=500,before=itr.id,after=twe,bulk=True,oldest_first=False)
        await itr.edit_original_message(content=f":broom: Successfully wiped {len(pur)} message{'s' if len(pur)>1 else ''}." if len(pur)>0 else ":negative_squared_cross_mark: No messages were wiped.",view=Wipedone(followup=itr.followup,message=await itr.original_message()) if not hidden else None)

    @wipe.sub_command()
    async def hastext(self,itr,text:str,user:discord.User=None,count:int=20,hidden:bool=False):
        await itr.response.defer(ephemeral=hidden)
        twe=datetime.now()-timedelta(days=14)
        pur=await itr.channel.purge(check=WipeChecks(count=count,text=text.strip().lower(),user_id=user.id if user else None).hastextcheck,limit=500,before=itr.id,after=twe,bulk=True,oldest_first=False)
        await itr.edit_original_message(content=f":broom: Successfully wiped {len(pur)} message{'s' if len(pur)>1 else ''}." if len(pur)>0 else ":negative_squared_cross_mark: No messages were wiped.",view=Wipedone(followup=itr.followup,message=await itr.original_message()) if not hidden else None)

    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.slash_command()
    async def unban(self,itr,user:str,reason:str=None):
        await itr.response.send_message(':x: The command does nothing yet.',ephemeral=True)

    @unban.autocomplete('user')
    async def unban_autocomp(self,itr,string:str):
        string=string.strip().lower()
        returndict={}
        try:
            banlist=await itr.guild.bans()
        except:
            return
        if string=="":
            for i in banlist:
                if len(list(returndict.items()))>25:
                    break
                returndict[str(i.user)]=str(i.user.id)
        else:
            for i in banlist:
                if len(list(returndict.items()))>25:
                    break
                if string in str(i.user).lower():
                    returndict[str(i.user)]=str(i.user.id)
        return returndict

    @unban.error
    async def unban_error(self,itr,error):
        if isinstance(error,commands.MissingPermissions):
            return await itr.response.send_message(':x: You need to have the `Ban Members` permission to use this command.',ephemeral=True)
        elif isinstance(error,commands.BotMissingPermissions):
            return await itr.response.send_message(':x: The bot must have the `Ban Members` permission to execute this command.',ephemeral=True)

    @commands.bot_has_permissions(kick_members=True)
    @commands.has_guild_permissions(manage_messages=True)
    @commands.slash_command()
    async def mute(self,itr,member:discord.Member,duration:str,reason:str=None):
        if member.id==itr.author.id:
            return await itr.response.send_message(':x: You cannot mute yourself.',ephemeral=True)
        elif member.id==itr.guild.owner_id:
            return await itr.response.send_message(':x: You cannot mute the server owner.',ephemeral=True)
        elif member.bot:
            return await itr.response.send_message(':x: You cannot mute bots.',ephemeral=True)
        elif member.guild_permissions.administrator:
            return await itr.response.send_message(':x: You cannot mute a server admin.',ephemeral=True)
        elif itr.author.id!=itr.guild.owner_id:
            if itr.author.top_role<=member.top_role:
                return await itr.response.send_message(':x: You cannot mute this member as you do not have a role higher than their highest role.',ephemeral=True)
        if itr.me.top_role<=member.top_role:
            return await itr.response.send_message(':x: I cannot mute this member because I do not have a role higher than their highest role.',ephemeral=True)
        try:
            mutetime=int(round(durations.Duration(duration.strip()).to_seconds()))
        except:
            return await itr.response.send_message(':x: Failed to parse time from given duration, please check it and try again.',ephemeral=True)
        if mutetime==0:
            return await itr.response.send_message(':x: The duration cannot be null.\n**This error could also have occurred if the time entered was invalid. If this was the case, please try again.**',ephemeral=True)
        elif mutetime<300:
            return await itr.response.send_message(':x: The mute duration cannot be shorter than 5 minutes.',ephemeral=True)
        elif mutetime>86400:
            return await itr.response.send_message(':x: The mute duration cannot be longer than a day.',ephemeral=True)
        await itr.response.defer(ephemeral=False)
        tim=datetime.now(timezone.utc)+timedelta(seconds=mutetime)
        r=requests.patch(f'https://discord.com/api/v9/guilds/{itr.guild_id}/members/{member.id}',headers={'Authorization':f'Bot {os.environ["BOT_TOKEN"]}'},json={"communication_disabled_until":tim.isoformat()})
        if r.status_code==200:
            embed=discord.Embed(color=discord.Color(3092791),description=f':white_check_mark: {member.mention} was successfully muted until <t:{int(calendar.timegm(tim.utctimetuple()))}:F>.')
            if reason:
                embed.add_field(name='For reason:',value=reason.strip())
            return await itr.edit_original_message(embed=embed)
        else:
            return await itr.edit_original_message(content=f':x: Failed to mute said member. ```json\n{r.json()}\n```')

    @mute.error
    async def mute_error(self,itr,error):
        if isinstance(error,commands.MissingPermissions):
            return await itr.response.send_message(':x: You need to have the `Manage Messages` permission in the server to use this command.',ephemeral=True)
        elif isinstance(error,commands.BotMissingPermissions):
            return await itr.response.send_message(':x: The bot must have the `Kick Members` permission to execute this command.',ephemeral=True)
        elif isinstance(error,commands.MemberNotFound):
            return await itr.response.send_message(':x: This user is not in the server.',ephemeral=True)

    @commands.bot_has_permissions(kick_members=True)
    @commands.has_guild_permissions(manage_messages=True)
    @commands.slash_command()
    async def unmute(self,itr:discord.ApplicationCommandInteraction,member:discord.Member,reason:str=None):
        if member.id==itr.guild.owner_id:
            return await itr.response.send_message(':x: You cannot unmute the server owner as they are immune to mutes.',ephemeral=True)
        elif member.bot:
            return await itr.response.send_message(':x: You cannot unmute bots.',ephemeral=True)
        elif member.guild_permissions.administrator:
            return await itr.response.send_message(':x: You cannot unmute a server admin as they are immune to mutes.',ephemeral=True)
        elif itr.author.id!=itr.guild.owner_id:
            if itr.author.top_role<=member.top_role:
                return await itr.response.send_message(':x: You cannot unmute this member as you do not have a role higher than their highest role.',ephemeral=True)
        if itr.me.top_role<=member.top_role:
            return await itr.response.send_message(':x: I cannot unmute this member because I do not have a role higher than their highest role.',ephemeral=True)
        r=requests.get(f'https://discord.com/api/v9/guilds/{itr.guild_id}/members/{member.id}',headers={'Authorization':f'Bot {os.environ["BOT_TOKEN"]}'}).json()
        if not r['communication_disabled_until']:
            return await itr.response.send_message(':x: This member is not muted.',ephemeral=True)
        elif datetime.fromisoformat(r['communication_disabled_until'])<datetime.now(timezone.utc):
            requests.patch(f'https://discord.com/api/v9/guilds/{itr.guild_id}/members/{member.id}',headers={'Authorization':f'Bot {os.environ["BOT_TOKEN"]}'},json={"communication_disabled_until":None})
            return await itr.response.send_message(':x: This member is not muted.',ephemeral=True)
        else:
            await itr.response.defer()
            r=requests.patch(f'https://discord.com/api/v9/guilds/{itr.guild_id}/members/{member.id}',headers={'Authorization':f'Bot {os.environ["BOT_TOKEN"]}'},json={"communication_disabled_until":None})
            if r.status_code==200:
                embed=discord.Embed(color=discord.Color(3092791),description=f':white_check_mark: {member.mention} was successfully unmuted.')
                if reason:
                    embed.add_field(name='For reason:',value=reason.strip())
                return await itr.edit_original_message(embed=embed)
            else:
                return await itr.edit_original_message(content=f':x: Failed to mute said member. ```json\n{r.json()}\n```')

    @unmute.error
    async def mute_error(self,itr,error):
        if isinstance(error,commands.MissingPermissions):
            return await itr.response.send_message(':x: You need to have the `Manage Messages` permission in the server to use this command.',ephemeral=True)
        elif isinstance(error,commands.BotMissingPermissions):
            return await itr.response.send_message(':x: The bot must have the `Kick Members` permission to execute this command.',ephemeral=True)
        elif isinstance(error,commands.MemberNotFound):
            return await itr.response.send_message(':x: This user is not in the server.',ephemeral=True)

def setup(client):
    client.add_cog(Moderation(client))
