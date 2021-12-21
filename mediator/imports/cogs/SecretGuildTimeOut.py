import os,durations,requests,calendar
import disnake as discord
from datetime import datetime,timedelta,timezone
from disnake.ext import commands

class SGTimeOut(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.Cog.listener()
    async def on_button_click(self,itr:discord.MessageInteraction):
        if itr.data.custom_id=="921448423402635274_remove_mute":
            requests.post(f'https://discord.com/api/v9/interactions/{itr.id}/{itr.token}/callback',json={"type":5,"data":{"flags":64}})
            requests.patch(f'https://discord.com/api/v9/guilds/{itr.guild_id}/members/{itr.author.id}',headers={'Authorization':os.environ['BOT_TOKEN']},json={"communication_disabled_until":None})
            return await itr.edit_original_message(content=':white_check_mark: Cleared your `communication_disabled_until` member field.')
        return

def setup(client):
    client.add_cog(SGTimeOut(client))
