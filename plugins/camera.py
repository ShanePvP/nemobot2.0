import discord
from discord.ext import commands
import plugins.json
import os
import datetime

class Camera:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pic')
    async def pic(self, ctx):
        path = os.getcwd()+"/camera/pic.jpg"
        os.system('raspistill -o os.getcwd()+"/camera/pic.jpg"')
        f = discord.File(path, filename="image.png")
        e = discord.Embed()
        e.set_image(url="attachment://image.png")
        await messagable.send(file=f, embed=e)
      
def setup(bot):
    bot.add_cog(Camera(bot))
