#!/usr/local/bin/python3.7
import discord
from discord.ext import commands
import os
import plugins.json
import asyncio

config_file = plugins.json.read_json('config')

config_start = int(config_file['start'])
config_interval =  int(config_file['interval'])
config_channel = int(config_file['channel'])

class Walls:

    def __init__(self, bot):
        self.bot = bot
        self.task = bot.loop.create_task(self.walls_loop())
        self.weewoos = True
        self.count = int(0)

    def __unload(self):
        self.task.cancel()

    async def walls_loop(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(config_channel)
        while not self.bot.is_closed():
            await asyncio.sleep(1)
            self.count += 1
            print(self.count)
            if (self.count == config_start) or ((self.count - config_start) % config_interval == 0 and self.count > config_start):
                #em = discord.Embed(colour=10038562)
                #em.set_thumbnail(url='http://icons.iconarchive.com/icons/chrisl21/minecraft/512/Tnt-icon.png')
                #em.add_field(name =':warning::exclamation:__**CHECK WALLS**__:exclamation::warning:', value='Walls have not been checked in ```https\n'+str(self.count)+' MINUTES!```', inline=False)
                #em.set_footer(text='Indicate walls are safe by typing \'!check\'')
                #await channel.send(embed = em)
                if self.count == config_start:
                    await channel.send(str(self.count) + ' minutes!\n@here')
                else:
                    await channel.send(str(self.count) + ' minutes!\n@role')

    @commands.command(name='check')
    async def check(self, ctx):
        self.count = 0
        await ctx.send('Walls checked')

    @commands.command(name='weewoo')
    async def weewoo(self, ctx):
        self.weewoos = True
        while True:
            await asyncio.sleep(5)
            if self.weewoos == True:
                self.count = 0
                await ctx.send('WEEWOO!\nWE ARE BEING RAIDED!\n@everyone')
            else:
                break

    @commands.command(name='safe')
    async def safe(self, ctx):
        await ctx.send('SAFE!')
        self.weewoos = False

def setup(bot):
    bot.add_cog(Walls(bot))
