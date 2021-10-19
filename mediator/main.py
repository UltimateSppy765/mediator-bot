import os,json,traceback,inspect
import disnake as discord
from imports import cogfunc
from disnake.ext import commands

intentss=discord.Intents(guilds=True,members=False,bans=True,emojis=False,integrations=False,webhooks=False,invites=False,voice_states=False,presences=False,messages=True,typing=False)
client=commands.Bot(command_prefix='!',sync_commands=False,activity=discord.Activity(type=discord.ActivityType.watching,name='your messages!'),intents=intentss,allowed_mentions=discord.AllowedMentions(roles=False))

with open('mediator/coglist.json','r') as file:
    data=json.load(file)

@client.event
async def on_ready():
    print('Bot is ready.')
    print(f'Logged in as {client.user.name} - {client.user.id}')

@commands.is_owner()
@client.slash_command(name="cog-stuff")
async def cogutils(itr):
    pass

@cogutils.error
async def cogutils_error(itr,error):
    if isinstance(error,commands.NotOwner):
        await itr.response.send_message(':x: You cannot use this command.',ephemeral=True)

async def acfunc(itr,string:str):
    string=string.strip()
    returndict={}
    if string=="":
        for l in cogfunc.getcogs():
            if len(list(returndict.items()))>25:
                break
            returndict[l['name']]=l['path']
    else:
        for i in cogfunc.getcogs():
            if len(list(returndict.items()))>25:
                break
            if string.lower() in i['path'].lower() or string.lower() in i['name'].lower():
                returndict[i['name']]=i['path']
    return returndict

@cogutils.sub_command(name="loaded-cogs")
async def loadedcogs(itr):
    cogstr=""
    maps=client.cogs
    cglist=list(maps)
    if cglist==[]:
        return await itr.response.send_message(':gear: No cogs are loaded at the moment.',ephemeral=True)
    for i in cglist:
        cogstr=cogstr+f"• {i} - {inspect.getfile(maps[i].__class__)}\n"
    e1=discord.Embed(description=f"```\n{cogstr}```",color=discord.Color(3092791))
    await itr.response.send_message(content=":scroll: Here are the cogs currently loaded:",embed=e1,ephemeral=True)

@cogutils.sub_command(name="list-cogs")
async def listcogs(itr):
    lst=cogfunc.getcogs()
    if lst==[]:
        return await itr.response.send_message(':gear: No cogs are specified in the config file.')
    cogstr=""
    for i in lst:
        cogstr=cogstr+f"• {i['name']} ({i['path']}) - {i['description']}\n"
    e1=discord.Embed(description=f"```\n{cogstr}```",color=discord.Color(3092791))
    await itr.response.send_message(content=":scroll: Here are the cogs listed in the config file:",embed=e1,ephemeral=True)

@cogutils.sub_command()
async def load(itr,name:str=commands.Param(autocomp=acfunc)):
    name=name.strip()
    try:
        client.load_extension(name)
    except Exception as e:
        if isinstance(e,commands.ExtensionNotFound):
            await itr.response.send_message(f':x: The extension `{name}` was not found.',ephemeral=True)
        elif isinstance(e,commands.ExtensionAlreadyLoaded):
            await itr.response.send_message(f':x: The extension `{name}` is already loaded.',ephemeral=True)
        elif isinstance(e,commands.NoEntryPointError):
            await itr.response.send_message(f':x: The extension `{name}` does not have a setup function.',ephemeral=True)
        elif isinstance(e,commands.ExtensionFailed):
            e1=discord.Embed(title="Exception raised:",description=f'```py\n{traceback.format_exc()}\n```')
            await itr.response.send_message(f':x: Failed to load extension: `{name}`',embed=e1,ephemeral=True)
    await itr.response.send_message(f':white_check_mark: Successfully loaded the extension: `{name}`',ephemeral=True)

@cogutils.sub_command()
async def unload(itr,name:str=commands.Param(autocomp=acfunc)):
    name=name.strip()
    try:
        client.unload_extension(name)
    except Exception as e:
        if isinstance(e,commands.ExtensionNotLoaded):
            await itr.response.send_message(f':x: The extension `{name}` is not already loaded.',ephemeral=True)
        elif isinstance(e,commands.ExtensionNotFound):
            await itr.response.send_message(f':x: The extension `{name}` was not found.',ephemeral=True)
    await itr.response.send_message(f':white_check_mark: Successfully unloaded the extension: `{name}`',ephemeral=True)

@cogutils.sub_command()
async def reload(itr,name:str=commands.Param(autocomp=acfunc)):
    name=name.strip()
    try:
        client.reload_extension(name)
    except Exception as e:
        if isinstance(e,commands.ExtensionNotLoaded) or isinstance(e,commands.ExtensionNotFound):
            await itr.response.send_message(f':x: The extension `{name}` is not already loaded or it does not exist.',ephemeral=True)
        elif isinstance(e,commands.NoEntryPointError):
            await itr.response.send_message(f':x: The extension `{name}` does not have a setup function.',ephemeral=True)
        elif isinstance(e,commands.ExtensionFailed):
            e1=discord.Embed(title="Exception raised:",description=f'```py\n{traceback.format_exc()}\n```')
            await itr.response.send_message(f':x: Failed to reload extension: `{name}`',embed=e1,ephemeral=True)
    await itr.response.send_message(f':white_check_mark: Successfully reloaded the extension: `{name}`',ephemeral=True)

successnum=0
for i in data['cog_list']:
    if i['load_on_start']==True:
        try:
            client.load_extension(i['path'])
            successnum+=1
        except:
            print(f"Failed to load extension: {i['name']}")
            print(traceback.format_exc())
if successnum>0:
    print(f'Successfully loaded {successnum} cog{"s" if successnum>1 else ""}.')

client.run(os.environ['BOT_TOKEN'])
