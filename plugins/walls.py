#!/usr/local/bin/python3
import discord
from discord.ext import commands
import os

config_file = plugins.json.read_json('config')

bot.config_start = int(config_file['start'])
bot.config_interval =  int(config_file['interval'])
bot.config_channel = int(config_file['channel'])

channel = bot.get_channel(bot.config_channel)

class Walls:
    def __init__(self, bot):
        self.bot = bot
        
    async def walls_loop():
        await bot.wait_until_ready()
        count = int(-1)
        while not bot.is_closed():
            count += 1
            bot.time_taken = str(count)
            if 0 < count < bot.config_start:
                await asyncio.sleep(60)
                print ('Count ' + str(count))
            elif count == bot.config_start:
                await asyncio.sleep(60)
                print ('Count ' + str(count))
                em = discord.Embed(colour=10038562)
                em.set_thumbnail(url='http://icons.iconarchive.com/icons/chrisl21/minecraft/512/Tnt-icon.png')
                em.add_field(name =':warning::exclamation:__**CHECK WALLS**__:exclamation::warning:', value='Walls have not been checked in ```https\n'+str(count)+' MINUTES!```', inline=False)
                em.set_footer(text='Indicate walls are safe by typing \''+bot.config_prefix+'check\'')
                await channel.send(embed = em)
                await channel.send(str(count) + ' minutes!\n@here')
                await asyncio.sleep(bot.config_interval*60)
            elif count >= bot.config_start and (count-bot.config_start) % bot.config_interval == 0:
                em = discord.Embed(colour=10038562)
                em.set_thumbnail(url='http://icons.iconarchive.com/icons/chrisl21/minecraft/512/Tnt-icon.png')
                em.add_field(name =':warning::exclamation:__**CHECK WALLS**__:exclamation::warning:', value='Walls have not been checked in ```https\n'+str(count)+' MINUTES!```', inline=False)
                em.set_footer(text='Indicate walls are safe by typing \''+bot.config_prefix+'check\'')
                await channel.send(embed = em)
        
def setup(bot):
    bot.add_cog(Walls(bot))
