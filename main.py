import os,discord
from discord.ext import commands

client=commands.Bot(command_prefix="!",activity=discord.Activity(type=discord.ActivityType.watching, name="your messages!"))

@client.event
async def on_ready():
    print('Bot is ready.')
    print(f'Logged in as {client.user.name} - {client.user.id}')

@client.event
async def on_interaction(itr):
    print(itr)
    await itr.response.send_message(f"Received an Interaction. Might be unstable because it's d.py v2...```py\n{itr}\n```",ephemeral=True)

client.run(os.environ['BOT_TOKEN'])
