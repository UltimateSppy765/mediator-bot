import os,traceback
import disnake as discord
from discord.ext import commands

coggs=["Moderation","Miscellaneous"] 
client=commands.Bot(sync_commands=False,command_prefix="!",activity=discord.Activity(type=discord.ActivityType.watching,name="your messages!",allowed_mentions=discord.AllowedMentions(roles=False)))

@client.event
async def on_ready():
    print('Bot is ready.')
    print(f'Logged in as {client.user.name} - {client.user.id}')

for i in coggs:
    try:
        client.load_extension(f"imports.cogs.{i}")
    except:
        print(f"Failed to load cog: {i}")
        print(traceback.format_exc())

client.run(os.environ['BOT_TOKEN'])
