#
#
#   Stan's Discord Bot for CCTV
#   Don't copy please <3
#
#

import discord
from discord.ext import commands
import asyncio
import os
#import json
import plugins.json
'''
config_file = json.load(open(os.getcwd()+'/bot_config/config.json'))
'''
config_file = plugins.json.read_json('config')
prefix = config_file['prefix']
token = config_file['token']

'''
with open('bot_config/token.txt', 'r') as token_file:
    token = token_file.read()
'''

'''
def get_prefix(bot, message):
    if not message.guild:
        return '?'
    return commands.when_mentioned_or('!')(bot, message)
'''


initial_extensions = plugins.json.read_json('plugins')

bot = commands.Bot(command_prefix=prefix, owner_id=252202327270883338)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)
    print('------')

if __name__ == '__main__':
    print('------')
    for extension in initial_extensions:
        #try:
        bot.load_extension(extension)
            #print('EXTENSION LOADED SUCCESSFULLY: '+extension)
        #except:
            #print('EXTENSION FAILEDF TO LOAD: '+extension)
            

bot.run(token)
