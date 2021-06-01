import os,discord
from discord.ext import commands

client=commands.Bot(command_prefix="!",activity=discord.Activity(type=discord.ActivityType.watching, name="your messages!"))

@client.event
async def on_ready():
    print('Bot is ready.')
    print(f'Logged in as {client.user.name} - {client.user.id}')

@client.event
async def on_interaction(itr):
    await itr.send_message(f"Received an Interaction.```py\n{itr}\n```")

client.run(os.environ['BOT_TOKEN'])
