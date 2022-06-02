import json

import discord
from discord import app_commands
from discord.ext import commands


class Miscellaneous(commands.Cog):
    """Contains miscellaneous commands."""

    def __init__(self, client):
        self.client = client
        with open(client.l10nlist["Miscellaneous"], "r") as file:
            self.l10ndata = json.loads(file)

    @app_commands.command(name="ping")
    async def ping(self, itr: discord.Interaction) -> None:
        DebugVieww = discord.ui.View(timeout=None)
        DebugVieww.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.blurple,
                label=self.l10ndata["ping"]["btnlabel"][str(itr.locale)],
                custom_id="debug_button",
                emoji="📄",
            )
        )
        await itr.response.send_message(
            self.l10ndata["ping"]["response"][str(itr.locale)].format(
                round(self.client.latency * 1000)
            ),
            ephemeral=True,
            view=DebugVieww,
        )


async def setup(client) -> None:
    await client.add_cog(Miscellaneous())
