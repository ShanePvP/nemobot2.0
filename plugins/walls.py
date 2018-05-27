#!/usr/local/bin/python3
import discord
from discord.ext import commands
import os

class Walls:
    def __init__(self, bot):
        self.bot = bot

        @bot.command(aliases=['c','C','CHECK'])
        @commands.cooldown(1, 300, commands.BucketType.user)
        async def check(ctx):
            if bot.walls == True:
                await ctx.trigger_typing()
                try:
                    uid = '{0.id}'.format(ctx.message.author)
                    avatar = '{0.avatar_url}'.format(ctx.message.author)
                    add_check(uid)
                    bot.task.cancel()
                    bot.task = bot.loop.create_task(walls())
                    data = read_json('log')
                    name = data[uid]['ign']
                    checks = data[uid]['checks']
                    uuid = data[uid]['uuid']
                    em = discord.Embed(colour=2067276)
                    em.set_author(name=name, icon_url=avatar)
                    em.add_field(name ='Walls Checked', value=stars(checks)+'``'+name+'``\n``('+uuid+')``', inline=False)
                    em.add_field(name ='Checks:', value='``'+checks+'``', inline=False)
                    em.set_thumbnail(url='https://visage.surgeplay.com/head/'+uuid)
                    em.set_footer(text='Time taken to check: '+bot.time_taken+' minutes')
                    await asyncio.sleep(1)
                    await ctx.send (embed=em)
                    try:
                        bot.weewoo.cancel()
                        bot.weewoo_state = False
                    except:
                        pass
                except:
                    ctx.command.reset_cooldown(ctx)
                    em = discord.Embed(colour=10038562)
                    em.add_field(name =':x: ERROR :x:', value='Your discord id (``'+uid+'``) has no IGN registered!\nPlease type ``'+bot.config_prefix+'ign <name>`` to register a username.', inline=False)
                    await asyncio.sleep(1)
                    await ctx.send (embed=em)
            elif bot.walls == False:
                ctx.command.reset_cooldown(ctx)
                em = discord.Embed(colour=10038562)
                em.add_field(name =':x: ERROR :x:', value=':gear: Walls are ``OFF``', inline=False)
                await asyncio.sleep(1)
                await ctx.send (embed=em)
      
def setup(bot):
    bot.add_cog(Walls(bot))
