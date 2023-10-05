import json
import discord
from discord.ext.ipc import Server, ClientPayload
import ezcord
import os
import dotenv
from web import app
from utils.gears import load_gears

# env vars
dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

class Bot(ezcord.Bot):
    def __init__(self: ezcord.Bot):
        super().__init__(intents=discord.Intents.all())
        self.ipc = Server(self, secret_key="yasuna")

    async def on_ready(self):
        await self.ipc.start()
        print(f"{self.user} ist online")

    @Server.route()
    async def guild_count(self, _):
        return str(len(self.guilds))
    
    @Server.route()
    async def get_guild_data(self, data: ClientPayload):
        guild_id: int = int(data.guild_id)
        for guild in self.guilds:
            if int(guild_id) == int(guild.id):
                guild: discord.Guild = self.get_guild(guild_id)
                print(str(guild.owner.id))
                return {
                    'name': guild.name,
                    'id': guild.id,
                    'description': guild.description,
                    'members': [member.id for member in guild.members],
                    'owner_id': str(guild.owner_id),
                    'icon': guild.icon.url,
                    'roles': [role.id for role in guild.roles],
                    'created_at': str(guild.created_at)
                }
                
            else:
                return None

    @Server.route()
    async def on_ipc_error(self, endpoint: str, exc: Exception):
        raise exc

# init the bot
bot = Bot()

load_gears(bot, './src/gears/')

# run if __name__ is equal to '__main__'
if __name__ == '__main__':
    bot.run(token)