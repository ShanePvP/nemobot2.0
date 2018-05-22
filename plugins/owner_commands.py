#!/usr/local/bin/python3
from discord.ext import commands
import plugins.json
import os
import asyncio

async def cog_reload():
    initial_extensions = plugins.json.read_json('plugins')
    for extension in initial_extensions:
        try:
            self.bot.unload_extension(extension)
            self.bot.load_extension(extension)
            await ctx.send('Reloaded: ``'+extension+'``')
        except:
            await ctx.send('Failed: ``'+extension+'``')

class OwnerCog:

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='reload')
    @commands.is_owner()
    async def reload(self, ctx):
        await cog_reload()
            
    @commands.command(name='update')
    @commands.is_owner()
    async def bot_update(self, ctx):
        os.system('cd && cd CCTV && git pull https://github.com/5tanly/CCTV')
        await asyncio.sleep(2)
        await cog_reload()

def setup(bot):
    bot.add_cog(OwnerCog(bot))
