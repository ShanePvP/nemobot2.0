#!/usr/local/bin/python3
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
        await ctx.send('Taking picture')
        await ctx.trigger_typing()
        path = os.getcwd()+"/camera/pic.jpg"
        os.system('raspistill --nopreview --mode 2 --annotate 12 --output ' + path)
        await ctx.send(file=discord.File(path, filename="pic.jpg"))
      
def setup(bot):
    bot.add_cog(Camera(bot))
