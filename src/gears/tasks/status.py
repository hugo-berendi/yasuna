import discord
import ezcord
import random
from discord.ext import commands, tasks


class Status(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.status.start()

    @tasks.loop(minutes=2)
    async def status(self):

        # create status list for bot status
        status_list = [
            discord.Status.idle,
            discord.Status.dnd,
            discord.Status.online
        ]

        # counts all member for activity list
        members = 0
        for guild in self.bot.guilds:
            members += guild.member_count

        # create activity list for bot activity
        activity_list = [
            discord.Game("by @hugo.berendi"),
            discord.Game(f"with {len(self.bot.guilds)} servers"),
            discord.Game(f"with {members} users")
        ]

        # set bot presence with status and activity
        await self.bot.change_presence(
            status=random.choice(status_list),
            activity=random.choice(activity_list)
        )


def setup(bot):
    bot.add_cog(Status(bot))