import discord,typing
from discord.ext import commands
from datetime import datetime,timedelta
from imports.modules import perspective

class Moderation(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.Cog.listener()
    async def on_interaction(self,itr):
        if itr.type==discord.InteractionType.application_command:
            if itr.data["name"]=="wipe":
                await self.wipeslash(itr)
					
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.group(invoke_without_command=True)
    async def wipe(self,ctx):
        "Base command for wiping messages in a channel. Max messages that can be purged is 200."
        return await ctx.reply("<:mno:851569517242351616> Missing or Invalid Subcommand.") 
    @wipe.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(read_message_history=True,send_messages=True,manage_messages=True)
    @commands.guild_only() 
    async def off(self,ctx,count:int=20):
        "Wipes off n messages in a channel with no checks." 
        if count>200 or count<1:
            return await ctx.reply("<:merror:851584410935099423> Please enter a count between 1 and 200.")
        msg=await ctx.reply("<:mwiping:851682672593731596> Wiping Messages...",mention_author=False)
        twe=datetime.now()-timedelta(days=14)
        pur=await ctx.channel.purge(limit=count,before=ctx.message,oldest_first=False,after=twe)
        s='s' if len(pur)!=1 else ''
        await msg.edit(content=f"<:mwipeyay:851572058382925866> Successfully wiped {len(pur)} message{s}." if len(pur)>0 else "<:mno:851569517242351616> No messages were wiped.")
        return
    @wipe.command()
    @commands.bot_has_permissions(read_message_history=True,send_messages=True,manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def user(self,ctx,user:typing.Union[discord.Object,discord.Member],count:int=20):
        "Wipes off messages sent by an individual user. Checks the most recent 500 messages."
        if count>200 or count<1:
            return await ctx.reply("<:merror:851584410935099423> Please enter a count between 1 and 200.")
        msg=await ctx.reply("<:mwiping:851682672593731596> Wiping Messages...",mention_author=False)
        twe=datetime.now()-timedelta(days=14)
        lim=1
        ss=0
        mlist=[]
        async for mes in ctx.channel.history(limit=500,before=ctx.message,after=twe,oldest_first=False):
            if mes.author.id==user.id and lim<=count:
                mlist.append(mes.id)
                lim+=1
            elif lim>count:
                ss+=1
                break
            ss+=1
        def mchk(m,list=mlist):
            if m.id in list:
                return True
            else:
                return False
        pur=await ctx.channel.purge(limit=ss,before=ctx.message,oldest_first=False,after=twe,check=mchk)
        s='s' if len(pur)!=1 else ''
        await msg.edit(content=f"<:mwipeyay:851572058382925866> Successfully wiped {len(pur)} message{s}." if len(pur)>0 else "<:mno:851569517242351616> No messages were wiped.")
        return
    @wipe.command()
    @commands.bot_has_permissions(read_message_history=True,send_messages=True,manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def perspective(self,ctx,count:typing.Optional[int]=20,perc:typing.Optional[int]=95):
        "[BETA] Wipes off messages containing toxic text. Checks the most recent 300 messages. The first argument is always message count irrespective of how many arguments are passed."
        if count>200 or count<1:
            return await ctx.reply("<:merror:851584410935099423> Please enter a count between 1 and 200.")
        if perc>99 or perc<20:
            return await ctx.reply("<:merror:851584410935099423> Toxicity parameter cannot be greater than 99 or less than 20.")
        msg=await ctx.reply("<:mwiping:851682672593731596> Wiping Messages...",mention_author=False)
        twe=datetime.now()-timedelta(days=14)
        lim=1
        ss=0
        mlist=[]
        async for mes in ctx.channel.history(limit=300,before=ctx.message,after=twe,oldest_first=False):
            if perspective.istoxic(txt=mes.content,per=perc)==True and lim<=count:
                mlist.append(mes.id)
                lim+=1
            elif lim>count:
                ss+=1
                break
            ss+=1
        def mchk(m,list=mlist):
            if m.id in list:
                return True
            else:
                return False
        pur=await ctx.channel.purge(limit=ss,before=ctx.message,after=twe,oldest_first=False,check=mchk)
        s='s' if len(pur)!=1 else ''
        await msg.edit(content=f"<:mwipeyay:851572058382925866> Successfully wiped {len(pur)} message{s}." if len(pur)>0 else "<:mno:851569517242351616> No messages were wiped.")
        return
    @wipe.command()
    @commands.bot_has_permissions(read_message_history=True,send_messages=True,manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def hastext(self,ctx,count:typing.Optional[int]=20,*,text:str):
        "Wipes off messages containing specific text (Text can be input using ""). Checks the most recent 500 messages."
        if count>200 or count<1:
            return await ctx.reply("<:merror:851584410935099423> Please enter a count between 1 and 200.")
        msg=await ctx.reply("<:mwiping:851682672593731596> Wiping Messages...",mention_author=False)
        twe=datetime.now()-timedelta(days=14)
        lim=1
        ss=0
        mlist=[]
        async for mes in ctx.channel.history(limit=500,before=ctx.message,after=twe,oldest_first=False):
            if text.lower() in mes.content.lower() and lim<=count:
                mlist.append(mes.id)
                lim+=1
            elif lim>count:
                ss+=1
                break
            ss+=1
        def mchk(m,list=mlist):
            if m.id in list:
                return True
            else:
                return False
        pur=await ctx.channel.purge(limit=ss,before=ctx.message,after=twe,oldest_first=False,check=mchk)
        s='s' if len(pur)!=1 else ''
        await msg.edit(content=f"<:mwipeyay:851572058382925866> Successfully wiped {len(pur)} message{s}." if len(pur)>0 else "<:mno:851569517242351616> No messages were wiped.")
        return
    async def wipeslash(self,itr):
        scn=itr.data["options"][0]["name"]
        try:
            perms=itr.channel.permissions_for(itr.user).manage_messages
        except:
            return await itr.response.send_message("<:merror:851584410935099423> This command cannot be used in Direct Messages/Channels that I don't have the permission to view in.",ephemeral=True)
        if perms==False:
            return await itr.response.send_message("<:merror:851584410935099423> You cannot use this command.",ephemeral=True)
        mem=itr.guild.get_member(itr.application_id)
        if itr.channel.permissions_for(mem).manage_messages==False or itr.channel.permissions_for(mem).read_message_history==False:
            if itr.channel.permissions_for(self.user).manage_messages==False and itr.channel.permissions_for(mem).read_message_history==False:
                missperms="Read Message History\nManage Messages"
            else:
                missperms="Read Message History" if itr.channel.permissions_for(mem).read_message_history==False else "Manage Messages"
            return await itr.response.send_message(f"<:merror:851584410935099423> I do not have the required permissions to perform this, please check my permissions for this channel:```\n{missperms}\n```",ephemeral=True)
        try:
            for i in itr.data["options"][0]["options"]:
                if i["name"]=='count':
                    count=i["value"]
            varone=f"Count? {count}"
            del varone
        except:
            count=20
        try:
            for i in itr.data["options"][0]["options"]:
                if i["name"]=='ephemeral':
                    eph=i["value"]
            vartwo=f"Ephemeral? {eph}"
            del vartwo
        except:
            eph=False
        if count>200 or count<1:
            return await itr.response.send_message("<:merror:851584410935099423> Please enter a count between 1 and 200.",ephemeral=True)
        if scn=="off":
            twe=datetime.now()-timedelta(days=14)
            await itr.response.defer(ephemeral=eph)
            pur=await itr.channel.purge(limit=count,oldest_first=False,bulk=True,after=twe,before=discord.Object(itr.id))
        if scn=="user":
            usid=int(itr.data["options"][0]["options"][0]["value"])
            twe=datetime.now()-timedelta(days=14)
            await itr.response.defer(ephemeral=eph)
            lim=1
            ss=0
            mlist=[]
            async for mes in itr.channel.history(limit=500,before=discord.Object(itr.id),after=twe,oldest_first=False):
                if mes.author.id==usid and lim<=count:
                    mlist.append(mes.id)
                    lim+=1
                elif lim>count:
                    ss+=1
                    break
                ss+=1
            def mchk(m,list=mlist):
                if m.id in list:
                    return True
                else:
                    return False
            pur=await itr.channel.purge(limit=ss,before=discord.Object(itr.id),bulk=True,after=twe,oldest_first=False,check=mchk)
        if scn=="perspective":
            try:
                for i in itr.data["options"][0]["options"]:
                    if i ["name"]=="percentage":
                        perc=i["value"]
                varthree=f"Percentage? {perc}"
                del varthree
            except:
                perc=95
            if perc>99 or perc<20:
                return await itr.response.send_message("<:merror:851584410935099423> Toxicity parameter cannot be greater than 99 or less than 20.",ephemeral=True)
            twe=datetime.now()-timedelta(days=14)
            await itr.response.defer(ephemeral=eph)
            lim=1
            ss=0
            mlist=[]
            async for mes in itr.channel.history(limit=300,before=discord.Object(itr.id),after=twe,oldest_first=False):
                if perspective.istoxic(txt=mes.content,per=perc)==True and lim<=count:
                    mlist.append(mes.id)
                    lim+=1
                elif lim>count:
                    ss+=1
                    break
                ss+=1
            def mchk(m,list=mlist):
                if m.id in list:
                    return True
                else:
                    return False
            pur=await itr.channel.purge(limit=ss,before=discord.Object(itr.id),after=twe,oldest_first=False,bulk=True,check=mchk)
        if scn=="hastext":
            twe=datetime.now()-timedelta(days=14)
            await itr.response.defer(ephemeral=eph)
            for j in itr.data["options"][0]["options"]:
                if j["name"]=="text":
                    cont=j["value"]
                    break
            try:
                for i in itr.data["options"][0]["options"]:
                    if i["name"]=="user":
                        ud=i["value"]
                varfour=f"User ID? {ud}"
                del varfour
            except:
                ud="None"
            print(f"Count: {count}\nText: {cont}\nUser: {ud}")
            lim=1
            ss=0
            mlist=[]
            def uchk(a:int,b):
                print(a)
                print(b)
                if b=="None":
                    return True
                elif a==b:
                    return True
                else:
                    return False
            async for mes in itr.channel.history(limit=500,before=discord.Object(itr.id),after=twe,oldest_first=False):
                if cont.lower() in mes.content.lower() and lim<=count:
                    if uchk(a=mes.author.id,b=ud)==True:
                        mlist.append(mes.id)
                        lim+=1
                elif lim>count:
                    break
                ss+=1
            def mchk(m,list=mlist):
                if m.id in list:
                    return True
                else:
                    return False
            pur=await itr.channel.purge(limit=ss,before=discord.Object(itr.id),after=twe,oldest_first=False,bulk=True,check=mchk)
        s='s' if len(pur)!=1 else ''
        return await itr.followup.send(content=f"<:mwipeyay:851572058382925866> Successfully wiped {len(pur)} message{s}." if len(pur)>0 else "<:mno:851569517242351616> No messages were wiped.")
    
def setup(client):
    client.add_cog(Moderation(client))
