#!/usr/local/bin/python3
import discord
from discord.ext import commands
import os

class Walls:
    def __init__(self, bot):
        self.bot = bot

        
def setup(bot):
    bot.add_cog(Walls(bot))
