import os
import discord

def load_gears(bot: discord.Bot, gear_dir: str):
    dirs = os.listdir(gear_dir)

    for dir in dirs:
        gears = os.listdir(f'{gear_dir}{dir}/')
        for f in gears:
            gears = f.removesuffix('.py')
            if gears == '__pycache__':
                continue
            bot.load_extension(f'gears.{dir}.{gears}')
            print(f'% Loaded "{gears}"')