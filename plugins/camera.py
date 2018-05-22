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
        os.system('raspistill -o os.getcwd()+"/camera/pic.jpg"')
        embed=discord.Embed(color=0xff8000)
        embed.add_field(name=datetime.datetime.now().strftime("%y-%m-%d"), value=datetime.datetime.now().strftime("%H:%M"), inline=False)
        await ctx.send (embed=embed,filename=os.getcwd()+"/camera/pic.jpg")
      
def setup(bot):
    bot.add_cog(Camera(bot))
