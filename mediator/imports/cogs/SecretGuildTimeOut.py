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
            try:
                await itr.author.timeout(duration=None)
            except e as Exception:
                return await itr.edit_original_message(content=f':x: Failed to clear your `communication_disabled_until` member field. ```\n{e.text}\n```')
            else:
                return await itr.edit_original_message(content=':white_check_mark: Cleared your `communication_disabled_until` member field.')
    
    @commands.slash_command(name='self-mute')
    async def selfmute(self,itr:discord.ApplicationCommandInteraction,duration:str):
        try:
            mutetime=int(round(durations.Duration(duration.strip()).to_seconds()))
        except:
            return await itr.response.send_message(':x: Failed to parse time from given duration, please check it and try again.',ephemeral=True)
        if mutetime==0:
            return await itr.response.send_message(':x: The duration cannot be null.\n**This error could also have occurred if the time entered was invalid. If this was the case, please try again.**',ephemeral=True)
        elif mutetime<0:
            return await itr.response.send_message(':x: The mute duration cannot be negative.',ephemeral=True)
        elif mutetime>2419200:
            return await itr.response.send_message(':x: The mute duration cannot be above 28 days (API Limitation).',ephemeral=True)
        await itr.response.defer(ephemeral=True)
        try:
           memtimeout=await itr.author.timeout(duration=mutetime)
        except e as Exception:
            return await itr.edit_original_message(content=f':x: Failed to mute you. ```json\n{e.text}\n```')
        else:
            return await itr.edit_original_message(content=f":white_check_mark: Sucessfully muted you until <t:{int(calendar.timegm(memtimeout.current_timeout.utctimetuple()))}:F>.")

def setup(client):
    client.add_cog(SGTimeOut(client))
