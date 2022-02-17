import os
import disnake as discord
from disnake.ext import commands

client=commands.InteractionBot(sync_commands=False,activity=discord.Activity(type=discord.ActivityType.watching,name='your messages!'),allowed_mentions=discord.AllowedMentions(everyone=False,roles=False))

client.run(os.environ['BOT_TOKEN']
