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
        await ctx.trigger_typing()
        path = os.getcwd()+"/camera/pic.jpg"
        os.system('raspistill -o ' + path)
        await ctx.send(file=discord.File(path, filename="image.png"))
      
def setup(bot):
    bot.add_cog(Camera(bot))
