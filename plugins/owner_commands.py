#!/usr/local/bin/python3
from discord.ext import commands
import plugins.json
import os

class OwnerCog:

    def __init__(self, bot):
        self.bot = bot
                
    @commands.command(name='reboot')
    @commands.is_owner()
    async def pi_reboot(self, ctx):
        await ctx.send('Rebooting...')
        os.system('sudo reboot')
        
    @commands.command(name='shutdown')
    @commands.is_owner()
    async def pi_shutdown(self, ctx):
        await ctx.send('Shutting Down...')
        os.system('sudo shutdown now')
            
    @commands.command(name='update')
    @commands.is_owner()
    async def bot_update(self, ctx):
        ##PULL FROM GITHUB
        config_file = plugins.json.read_json('config')
        prefix = config_file['prefix']
        os.system('cd && cd ' + os.getcwd() + ' && git pull https://github.com/5tanly/CCTV')
        
        ##RELOAD PLUGINS
        initial_extensions = plugins.json.read_json('plugins')
        for extension in initial_extensions:
            try:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
                await ctx.send(':white_check_mark: Reloaded: ``'+extension+'``')
            except:
                await ctx.send(':x: Failed: ``'+extension+'``')

def setup(bot):
    bot.add_cog(OwnerCog(bot))
