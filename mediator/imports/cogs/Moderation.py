import disnake as discord
from datetime import datetime,timedelta
from disnake.ext import commands

class WipeChecks():
    def __init__(self):
        self.counter=1
    
    def usercheck(self,m):
        if self.counter>self.count:
            return False
        if m.author.id==self.user_id:
            self.counter+=1
            return True

    def hastextcheck(self,m):
        if self.counter>self.count:
            return False
        if m.content.lower()==self.textchk:
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
    def __init__(self):
        self.responded=False
        super().__init__(timeout=5)

    @discord.ui.button(label="Got it!",style=discord.ButtonStyle.green)
    async def wipegotit(self,btn:discord.ui.Button,itr:discord.Interaction):
        self.responded=True
        await self.message.delete()

    async def on_timeout(self):
        if not self.responded:
            return await self.message.edit(view=None)

class Moderation(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(read_message_history=True,manage_messages=True)
    @commands.slash_command()
    async def wipe(self,itr):
        pass

    @wipe.error
    async def wipe_error(self,itr,error):
        if isinstance(error,commands.MissingPermissions):
            return await itr.response.send_message(':x: You need to have the `Manage Messages` permission to run this command.',ephemeral=True)
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
        twe=datetime.now()-timedelta(days=14)
        pur=await itr.channel.purge(limit=count,before=discord.Object(itr.id),after=twe,bulk=True,oldest_first=False)
        view=Wipedone() if not hidden else None
        await itr.edit_original_message(content=f":broom: Successfully wiped {len(pur)} message{'s' if len(pur)>1 else ''}." if len(pur)>0 else ":negative_squared_cross_mark: No messages were wiped.",view=view)
        if not hidden:
            view.message=await itr.original_message()
        return

    @wipe.sub_command()
    async def user(self,itr,user:discord.User,count:int=20,hidden:bool=False):
        await itr.response.defer(ephemeral=hidden)
        chk=WipeChecks()
        chk.user_id=user.id
        chk.count=count
        twe=datetime.now()-timedelta(days=14)
        pur=await itr.channel.purge(check=chk.usercheck,limit=500,before=discord.Object(itr.id),after=twe,bulk=True,oldest_first=False)
        view=Wipedone() if not hidden else None
        await itr.edit_original_message(content=f":broom: Successfully wiped {len(pur)} message{'s' if len(pur)>1 else ''}." if len(pur)>0 else ":negative_squared_cross_mark: No messages were wiped.",view=view)
        if not hidden:
            view.message=await itr.original_message()
        return

    @wipe.sub_command()
    async def hastext(self,itr,text:str,user:discord.User=None,count:int=20,hidden:bool=False):
        await itr.response.defer(ephemeral=hidden)
        chk=WipeChecks()
        chk.textchk=text.lower()
        chk.count=count
        if user:
            chk.user_id=user.id
        else:
            chk.user_id=None
        twe=datetime.now()-timedelta(days=14)
        pur=await itr.channel.purge(check=chk.hastextcheck,limit=500,before=discord.Object(itr.id),after=twe,bulk=True,oldest_first=False)
        view=Wipedone() if not hidden else None
        await itr.edit_original_message(content=f":broom: Successfully wiped {len(pur)} message{'s' if len(pur)>1 else ''}." if len(pur)>0 else ":negative_squared_cross_mark: No messages were wiped.",view=view)
        if not hidden:
            view.message=await itr.original_message()
        return

def setup(client):
    client.add_cog(Moderation(client))
