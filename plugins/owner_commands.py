from discord.ext import commands
import plugins.json
import os

class OwnerCog:

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='reload')
    @commands.is_owner()
    async def cog_reload(self, ctx):
        initial_extensions = plugins.json.read_json('plugins')
        for extension in initial_extensions:
            try:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
                await ctx.send('Reloaded: ``'+extension+'``')
            except:
                pass
            
    @commands.command(name='update')
    @commands.is_owner()
    async def bot_update(self, ctx):
    os.system('cd && cd os.getcwd() && git pull https://github.com/5tanly/CCTV')

def setup(bot):
    bot.add_cog(OwnerCog(bot))
