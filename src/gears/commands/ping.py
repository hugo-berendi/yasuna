import discord
from discord import ApplicationContext
from discord.ext import commands
from discord.commands import slash_command


class Ping(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(description="Sends the current ping of the bot", name="ping")
    async def ping(self, ctx: ApplicationContext,):
        emb = discord.Embed(
            title='Ping?',
            description=f'Pong! Latency is {self.bot.latency}',
            color=discord.Colour.blue()
        )
        
        await ctx.respond(embed=emb)

def setup(bot):
    bot.add_cog(Ping(bot))