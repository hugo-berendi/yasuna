import discord
from discord import ApplicationContext, SlashCommandGroup
from discord.ext import commands
import requests
from NHentai import NHentai


class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    nsfw_commands: SlashCommandGroup = discord.SlashCommandGroup('nsfw', 'All NSFW commands')

    @nsfw_commands.command(description="Hentai image with custom type", name="hentai")
    @commands.is_nsfw()
    async def hentai(
            self,
            ctx: ApplicationContext,
            tag: discord.Option(
                str, choices=[
                    'blowjob',
                    'cum',
                    'feet',
                    'hentai',
                    'wallpapers',
                    'spank',
                    'gasm',
                    'lesbian',
                    'lewd',
                    'pussy'
                ]
            ),
    ):
        req = requests.get(f'http://api.nekos.fun:8080/api/{tag}').json()
        url: str = req['image']

        emb = discord.Embed(
            title=f'Hentai Tag: {tag}',
            color=discord.Colour.nitro_pink()
        )
        emb.set_image(url=url)
        
        class HentaiButtons(discord.ui.View):      
            @discord.ui.button(label="New", row=0, style=discord.ButtonStyle.secondary, emoji='🔁')
            async def button_callback(self, button, interaction: discord.Interaction):
                req = requests.get(f'http://api.nekos.fun:8080/api/{tag}').json()
                url: str = req['image']
                
                emb.set_image(url=url)
                await interaction.response.edit_message(embed=emb)

        await ctx.respond(embed=emb, view=HentaiButtons())
        


def setup(bot):
    bot.add_cog(NSFW(bot))