#!/usr/local/bin/python3.7
#
#
#   Nemo Wall Bot v2.0
#   Don't copy please <3
#
#
#   embed color palette: https://www.color-hex.com/color-palette/700
#
import discord
from discord.ext import commands
import asyncio
import plugins.json
import os

config_file = plugins.json.read_json('config')
with open(os.getcwd()+'/bot_config/token.txt', 'r') as token_file:
    token = token_file.read().strip()
print(token)
prefix = config_file['prefix']
#token = config_file['token']

initial_extensions = plugins.json.read_json('plugins')

bot = commands.Bot(command_prefix=prefix, owner_id=252202327270883338)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('------')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

if __name__ == '__main__':
    print('------')
    for extension in initial_extensions:
        #try:
        bot.load_extension(extension)
            ##await ctx.send(':white_check_mark: Loaded: ``'+extension+'``')
            #print('Plugin Loaded: '+extension)
        #except:
            ##await ctx.send(':x: Failed: ``'+extension+'``')
            #print('Plugin Failed: '+extension)


bot.run(token)
