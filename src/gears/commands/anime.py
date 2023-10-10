import calendar
from AnilistPython import Anilist
import discord
from discord import ApplicationContext, SlashCommandGroup
from discord.ext import commands
from discord.commands import slash_command
import datetime


class Anime(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.anilist = Anilist()
        
    anime_commands: SlashCommandGroup = SlashCommandGroup('anime', 'Anime infos and more')

    @anime_commands.command(description="Search an anime by its name", name="search")
    async def anime(self, ctx: ApplicationContext, name: discord.Option(input_type=str, name='name', description='Enter a name of an anime')):
        anime_data = self.anilist.get_anime(anime_name=name)
        
        if not anime_data:
            emb = discord.Embed(
                title='A wild error apeared ⚠️',
                description='The anime you are searching does not exist. Please check if you wrote the name correct and try again.',
                color=discord.Colour.red()
            )
            return await ctx.respond(embed=emb)
        
        emb = discord.Embed(
                title=anime_data['name_english'],
                description=anime_data['desc'].replace('<br>', ''),
                color=discord.Colour.green(),
                thumbnail=discord.EmbedMedia(url=anime_data['cover_image'])
            )
        
        
        print(anime_data['starting_time'])
        starting_time = anime_data['starting_time'].split('/')
        ending_time = anime_data['ending_time'].split('/')
        
        starting_time = calendar.timegm(datetime.datetime(int(starting_time[2]), int(starting_time[0]), int(starting_time[1])).utctimetuple())
        emb.add_field(name='Started', value=f'<t:{starting_time}:D>')
        
        try:
            ending_time = calendar.timegm(datetime.datetime(int(ending_time[2]), int(ending_time[0]), int(ending_time[1])).utctimetuple())
            emb.add_field(name='Ended', value=f'<t:{ending_time}:D>')
        except:
            emb.add_field(name='Ended', value=f'Currently running!')
            if anime_data['next_airing_ep'] is not None:
                next_airing_ep = anime_data['next_airing_ep']
                emb.add_field(name='Next episode', value=f'Episode {next_airing_ep["episode"]}: <t:{next_airing_ep["airingAt"]}:R>')
        
        await ctx.respond(embed=emb)

def setup(bot):
    bot.add_cog(Anime(bot))