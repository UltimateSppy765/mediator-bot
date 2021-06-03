import os,discord
from discord.ext import commands

client=commands.Bot(command_prefix="!",activity=discord.Activity(type=discord.ActivityType.watching, name="your messages!",allowed_mentions=discord.AllowedMentions(roles=False)))

@client.event
async def on_ready():
    print('Bot is ready.')
    print(f'Logged in as {client.user.name} - {client.user.id}')

@client.event
async def on_interaction(itr):
    if itr.type==2:
        await itr.response.send_message(f"Bot ping is `{round(client.latency*1000)}ms`.",ephemeral=True)

@client.command()
@commands.guild_only()
@commands.has_permissions(kick_members=True)
async def mute(ctx,member,dur,*,reason=None):
    await ctx.send("This command doesn't do anything yet.")

client.run(os.environ['BOT_TOKEN'])
