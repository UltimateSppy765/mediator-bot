import os,discord,traceback
from discord.ext import commands

coggs=["imports.cogs.wipe"] 
client=commands.Bot(command_prefix="!",activity=discord.Activity(type=discord.ActivityType.watching, name="your messages!",allowed_mentions=discord.AllowedMentions(roles=False)))

@client.event
async def on_ready():
    print('Bot is ready.')
    print(f'Logged in as {client.user.name} - {client.user.id}')

@client.event
async def on_interaction(itr):
    if itr.type==discord.InteractionType.application_command and itr.data["name"]=="ping":
        await itr.response.send_message(f"Bot ping is `{round(client.latency*1000)}ms`.",ephemeral=True)

for i in coggs:
    try:
        client.load_extension(i)
    except:
        print(f"Failed to load cog: {i}")
        print(traceback.format_exc())
client.run(os.environ['BOT_TOKEN'])
