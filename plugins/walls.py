#!/usr/local/bin/python3.7
import discord
from discord.ext import commands
import os
import plugins.json
import asyncio
import sqlite3
from aiohttp import ClientSession
from random import randint
import datetime

config_file = plugins.json.read_json('config')

config_start = int(config_file['start'])
config_interval =  int(config_file['interval'])
config_channel = int(config_file['channel'])

class Walls:

    def __init__(self, bot):
        self.bot = bot
        self.task = bot.loop.create_task(self.walls_loop())
        self.weewoos = False
        self.count = int(0)

    def __unload(self):
        self.weewoos = False
        self.task.cancel()

    async def walls_loop(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(config_channel)
        while not self.bot.is_closed():
            await asyncio.sleep(60)
            self.count += 1
            print('Time: '+str(self.count))
            if (self.count == config_start) or ((self.count - config_start) % config_interval == 0 and self.count > config_start):
                if self.count == config_start:
                    await channel.send(str(self.count) + ' minutes!\n@here', delete_after=int(config_start))
                else:
                    await channel.send(str(self.count) + ' minutes!\n@everyone', delete_after=int(config_interval))

    @commands.command(name='ign')
    async def ign(self, ctx, ign=''):
        if ign == '':
            await ctx.send('Enter an IGN')
        else:
            try:
                _discid = '{0.id}'.format(ctx.message.author)
                _mcid, _mcname, _mcskin = await download_user(ign)
                add_user(_discid, _mcid, _mcname)
                await ctx.send(embed=embed('IGN Updated!', 'Name:', 'ID:', _mcname, _mcid, _mcskin, 0x00aedb))
            except:
                await ctx.send('ERROR: Invalid IGN or IGN already taken!')

    @commands.command(name='check')
    async def check(self, ctx):
        try:
            self.count = 0
            _discid = '{0.id}'.format(ctx.message.author)
            _mcid, _mcname, _checks, _mcskin = get_user_from_data(_discid)
            print(add_check(_discid, _checks))
            await ctx.send(embed=embed('Walls Checked!', 'Name:', 'Checks:', _mcname, _checks+1, _mcskin, 0x00b159))
        except:
            await ctx.send('ERROR: Please type ``!ign <name>`` to register!')

    @commands.command(name='weewoo')
    async def weewoo(self, ctx):
        if self.weewoos == False:
            _count = 0
            _timer = 3
            _time = str(datetime.datetime.now().strftime('%I:%M')) + ' EST'
            _image = 'https://bit.ly/2yjmBPY'
            self.weewoos = True
            _discname = '{0.mention}'.format(ctx.message.author)
            await ctx.send(embed=embed('(!) WEEWOO (!)', 'Name:', 'Time:', _discname, _time, _image, 0xd11141))
            while True:
                if self.weewoos == True:
                    self.count = 0
                    _count += 1
                    await ctx.send('@everyone '+ str(_count), delete_after=_timer)
                else:
                    break
                await asyncio.sleep(_timer)
        else:
            pass

    @commands.command(name='safe')
    async def safe(self, ctx):
        await ctx.send('SAFE!')
        self.weewoos = False

def embed(t, f1n, f2n, f1v, f2v, imageurl, color):
    em = discord.Embed(colour=color)
    em.set_author(name=t, icon_url='https://bit.ly/2CFvJCn')
    em.add_field(name=f1n, value=f1v, inline=False)
    em.add_field(name=f2n, value=f2v, inline=False)
    em.set_thumbnail(url=imageurl)
    return em

async def download_user(_ign):
    url = 'https://api.mojang.com/users/profiles/minecraft/'+_ign
    async with ClientSession() as session:
        async with session.get(url) as response:
            _d = await response.json()
            _mcid = _d['id']
            _mcname = _d['name']
            _mcskin = 'https://visage.surgeplay.com/face/512/'+_mcid+'?'+str(randint(0,999))
    return (_mcid, _mcname, _mcskin)

def add_user(_discid, _mcid, _mcname, _checks=0):
    conn = sqlite3.connect('bot_config/database.db')
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE checks (
                    discordid   text,
                    mcid        text,
                    mcname      text,
                    checks      integer
                    )""")
        conn.commit()
        print('db file created')
    except:
        pass
    c.execute("SELECT * FROM checks WHERE discordid=:discordid",{'discordid': _discid})
    did_fetch = str(c.fetchall())
    c.execute("SELECT * FROM checks WHERE mcname=:mcname",{'mcname': _mcname})
    mcname_fetch = str(c.fetchall())
    if _mcname in mcname_fetch:
        #Check if name is already in database and throw error if true
        error.error
    else:
        if _discid in did_fetch:
            #UPDATES MCNAME IN DATABASE
            c.execute("""UPDATE checks SET mcname=:mcname
                        WHERE discordid=:discordid
                        """,{'mcname':_mcname,'discordid':_discid})
            conn.commit()
            #UPDATES MCID IN DATABASE
            c.execute("""UPDATE checks SET mcid=:mcid
                        WHERE discordid=:discordid
                        """,{'mcid':_mcid,'discordid':_discid})
            conn.commit()
        else:
            print('Discord ID NOT IN YET!')
            #CREATES USER IF THEY DONT EXIST YET
            c.execute("""INSERT INTO checks VALUES (
                        :discordid,
                        :mcid,
                        :mcname,
                        :checks
                        )""",{'discordid':_discid,'mcid':_mcid,'mcname':_mcname,'checks':_checks})
            conn.commit()
    conn.close()

def add_check(_discid, _checks):

    conn = sqlite3.connect('bot_config/database.db')
    c = conn.cursor()
    c.execute("""UPDATE checks SET checks=:checks
                WHERE discordid=:discordid
                """,{'checks':_checks+1,'discordid':_discid})
    conn.commit()
    conn.close()
    return (_checks)

def get_user_from_data(_discid):
    conn = sqlite3.connect('bot_config/database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM checks WHERE discordid=:discordid",{'discordid': _discid})
    for row in c.fetchall():
        _mcid = str(row[1])
        _mcname = str(row[2])
        _checks = int(row[3])
        _mcskin = 'https://visage.surgeplay.com/face/512/'+_mcid+'?'+str(randint(0,999))
    conn.close()
    return(_mcid, _mcname, _checks, _mcskin)

def setup(bot):
    bot.add_cog(Walls(bot))
