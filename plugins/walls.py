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
                
        async def walls():
        await bot.wait_until_ready()
        channel = bot.get_channel(bot.config_channel)
        count = int(-1)
        while not bot.is_closed():
            count += 1
            bot.time_taken = str(count)
            if 0 < count < bot.config_start:
                await asyncio.sleep(60)
                print ('Count ' + str(count))
            elif count == bot.config_start:
                await asyncio.sleep(60)
                print ('Count ' + str(count))
                em = discord.Embed(colour=10038562)
                em.set_thumbnail(url='http://icons.iconarchive.com/icons/chrisl21/minecraft/512/Tnt-icon.png')
                em.add_field(name =':warning::exclamation:__**CHECK WALLS**__:exclamation::warning:', value='Walls have not been checked in ```https\n'+str(count)+' MINUTES!```', inline=False)
                em.set_footer(text='Indicate walls are safe by typing \''+bot.config_prefix+'check\'')
                await channel.send(embed = em)
                await channel.send(str(count) + ' minutes!\n@here')
                await asyncio.sleep(bot.config_interval*60)
            elif count >= bot.config_start and (count-bot.config_start) % bot.config_interval == 0:
                em = discord.Embed(colour=10038562)
                em.set_thumbnail(url='http://icons.iconarchive.com/icons/chrisl21/minecraft/512/Tnt-icon.png')
                em.add_field(name =':warning::exclamation:__**CHECK WALLS**__:exclamation::warning:', value='Walls have not been checked in ```https\n'+str(count)+' MINUTES!```', inline=False)
                em.set_footer(text='Indicate walls are safe by typing \''+bot.config_prefix+'check\'')
                await channel.send(embed = em)
                spam = int(((count-bot.config_start) / bot.config_interval))
                await checkspam(spam,count)
                
        async def checkspam(spam, count):
            channel = bot.get_channel(bot.config_channel)
            wait_time = ((bot.config_interval*60)/spam)
            print ('Count ' + str(count))
            print('Test ' + str(wait_time))
            for i in range(0, spam):
                await channel.send(str(count) + ' minutes\n<@&429491722352066562>')
                await asyncio.sleep(math.floor(wait_time))
            
        async def weewoos():
            await bot.wait_until_ready()
            channel = bot.get_channel(bot.config_channel)
            count = int(-1)
            while not bot.is_closed():
                await channel.send('__***WEEWOO***__\n<@&429491722352066562>')
                await asyncio.sleep(1)
                
        def stars(count):
            for i in reversed(range(0, bot.config_stars['emoji_count'])):
                value = bot.config_stars['values'][i]
                if count == '69':
                    star = ':eggplant:'
                elif count == '420':
                    star = ':leaves:'
                elif datetime.date.today().strftime("%d") in ['13','14'] and datetime.date.today().strftime("%m") in ['02']:
                    star = bot.config_stars['valentines'][i]
                elif datetime.date.today().strftime("%m") in ['12']:
                    star = bot.config_stars['xmas'][i]
                elif datetime.date.today().strftime("%m") in ['10']:
                    star = bot.config_stars['halloween'][i]
                elif datetime.date.today().strftime("%d") in ['01'] and datetime.date.today().strftime("%m") in ['04']:
                    star = bot.config_stars['easter'][i]
                else:
                    star = bot.config_stars['stars'][i]
                if int(count) >= int(value):
                    return star
                    break
                    
        async def add_user(uid, ign):
            if ign not in ['NONE']:
                url = 'https://api.mojang.com/users/profiles/minecraft/'+ign
                async with ClientSession() as session:
                    try:
                        async with session.get(url) as response:
                            d = await response.json()
                            print (d['name'])
                            print (d['id'])
                            update_user_info(uid, d['name'], d['id'])
                            em = discord.Embed(colour=2067276)
                            em.add_field(name ='IGN updated:', value='``'+d['name']+'``', inline=False)
                            em.add_field(name ='UUID updated:', value='``'+d['id']+'``', inline=False)
                            em.set_thumbnail(url='https://visage.surgeplay.com/full/'+d['id'])
                            bot.ign_message = em
                    except:
                        em = discord.Embed(colour=10038562)
                        em.add_field(name =':x: ERROR :x:', value='No Minecraft account with that username found!\nPlease try again.', inline=False)
                        bot.ign_message = em
            else:
                try:
                    d = read_json('log')
                    em = discord.Embed(colour=2067276)
                    em.add_field(name ='Your IGN is:', value=d[uid]['ign'], inline=False)
                    em.add_field(name ='UUID:', value=d[uid]['uuid'], inline=False)
                    em.set_thumbnail(url='https://visage.surgeplay.com/full/'+d[uid]['uuid'])
                    bot.ign_message = em
                except:
                    em = discord.Embed(colour=10038562)
                    em.add_field(name =':x: ERROR :x:', value='Your discord id (``'+uid+'``) has no IGN registered!\nPlease type ``'+bot.config_prefix+'ign <name>`` to register a username.', inline=False)
                    bot.ign_message = em

        def update_user_info(uid, ign, uuid):
            data = read_json('log')
            if uid in data:
                data[uid]['ign'] = ign
                data[uid]['uuid'] = uuid
            else:
                data[uid] = {}
                data[uid]['ign'] = ign
                data[uid]['uuid'] = uuid
                data[uid]['checks'] = '0'
            print (data[uid])
            write_json(data, 'log')
                
        bot.task = bot.loop.create_task(walls())
def setup(bot):
    bot.add_cog(Walls(bot))
