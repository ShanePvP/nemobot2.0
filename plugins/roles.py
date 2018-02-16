import discord
from discord.ext import commands
import plugins.json

class Roles:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='addrole')
    async def addrole(self, ctx, _role='none'):
        if _role.lower() in plugins.json.read_json('roles'):
            role = discord.utils.get(ctx.guild.roles, name=_role)
            user = ctx.message.author
            await user.add_roles(role)
            em = discord.Embed(colour=2067276)
            em.add_field(name =':white_check_mark: SUCCESS :white_check_mark:', value='Role ``'+_role+'`` added!', inline=False)
            await ctx.send (embed=em)
        else:
            m=str('')
            for i in plugins.json.read_json('roles'):
                m=m+'\n``'+i+'``'
            em = discord.Embed(colour=10038562)
            em.add_field(name =':x: ERROR :x:', value='Role ``'+_role+'`` not found!\n\n__Available Roles__'+m, inline=False)
            await ctx.send (embed=em)

    @commands.command(name='removerole')
    async def removerole(self, ctx, _role='none'):
        if _role.lower() in plugins.json.read_json('roles'):
            role = discord.utils.get(ctx.guild.roles, name=_role)
            user = ctx.message.author
            await user.remove_roles(role)
            em = discord.Embed(colour=2067276)
            em.add_field(name =':white_check_mark: SUCCESS :white_check_mark:', value='Role ``'+_role+'`` removed!', inline=False)
            await ctx.send (embed=em)
        else:
            m=str('')
            for i in plugins.json.read_json('roles'):
                m=m+'\n``'+i+'``'
            em = discord.Embed(colour=10038562)
            em.add_field(name =':x: ERROR :x:', value='Role ``'+_role+'`` not found!\n\n__Available Roles__'+m, inline=False)
            await ctx.send (embed=em)
        
def setup(bot):
    bot.add_cog(Roles(bot))
