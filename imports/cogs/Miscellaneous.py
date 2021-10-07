import disnake as discord
from disnake.ext import commands
from imports.modules.perspective import getscore

class Miscellaneous(commands.Cog):
    def __init__(self,client):
        self.client=client

def setup(client):
    client.add_cog()
