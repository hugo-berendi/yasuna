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
    async def guild_stats(self, data: ClientPayload):
        guild = self.get_guild(data.guild_id)
        if not guild: return None
        return {
            "member_count": guild.member_count,
            "name": guild.name,
        }

    @Server.route()
    async def on_ipc_error(self, endpoint: str, exc: Exception):
        raise exc

# init the bot
bot = Bot()

load_gears(bot, './src/gears/')

# run if __name__ is equal to '__main__'
if __name__ == '__main__':
    bot.run(token)