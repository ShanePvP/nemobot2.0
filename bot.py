#
#
#   Stan's Discord Bot for his own server
#   Don't copy please <3
#
#

import discord
from discord.ext import commands
import asyncio
import os
import json
import plugins.json

config_file = json.load(open(os.getcwd()+'/bot_config/config.json'))
with open('bot_config/token.txt', 'r') as token_file:
    token = token_file.read()
    
def get_prefix(bot, message):
    if not message.guild:
        return '?'
    return commands.when_mentioned_or('!')(bot, message)



initial_extensions = plugins.json.read_json('plugins')

bot = commands.Bot(command_prefix='!', owner_id=252202327270883338)
bot.remove_command('help')

@bot.event
async def on_ready():
    
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except:
            pass
            

bot.run(token)
