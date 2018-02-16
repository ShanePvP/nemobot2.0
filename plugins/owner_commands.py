from discord.ext import commands
import plugins.json

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


def setup(bot):
    bot.add_cog(OwnerCog(bot))
