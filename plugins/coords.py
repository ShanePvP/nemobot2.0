#!/usr/local/bin/python3.7
import discord
from discord.ext import commands
import plugins.json
import sqlite3
import datetime

class OwnerCog:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='coords')
    async def coords(self, ctx, _fname='', _x=0, _z=0, *, _note='n/a'):
        try:
            int(_x)
            int(_z)
            conn = sqlite3.connect('bot_config/database.db')
            c = conn.cursor()
            try:
                c.execute("""CREATE TABLE coords (
                            f_name      text,
                            coord_x     integer,
                            coord_z     integer,
                            f_note      text
                            )""")
                conn.commit()
                print('.db file created')
            except:
                pass
            if _fname == '':        #Display all coordinates
                c.execute("SELECT * FROM coords")
                await ctx.send(str(c.fetchall()).replace('), (','\n').replace('[','').replace(']','').replace('(','').replace(')','').replace('\',',': ').replace('\'',''))
            else:                   #Add coordinates
                c.execute("""INSERT INTO coords VALUES (
                            :f_name,
                            :coord_x,
                            :coord_z,
                            :f_note
                            )""",{'f_name':_fname,'coord_x':_x,'coord_z':_z,'f_note':_note})

                conn.commit()
                try:
                    await ctx.send(embed=embed(_fname, _x, _z, _note))
                except:
                    await ctx.send('ERROR: Please include a NAME, X-COORD, Z-COORD!')
            conn.close()
        except:
            await ctx.send('ERROR: X-COORD and Z-COORD must be NUMBERS!')

def embed(_fname, _x, _z, _note):
    _time = datetime.datetime.now()
    em = discord.Embed(colour=0x00aedb)
    em.set_author(name='Coordinates Added!', icon_url='https://bit.ly/2CFvJCn')
    em.add_field(name ='__**Faction Name:**__ ', value=_fname, inline=False)
    em.add_field(name ='__**X:**__ ', value=_x, inline=False)
    em.add_field(name ='__**Z:**__ ', value=_z, inline=False)
    em.add_field(name ='__**Notes:**__', value=_note, inline=False)
    em.set_footer(text='Added at: '+_time.strftime('%I:%M')+' EST')
    return em

def setup(bot):
    bot.add_cog(OwnerCog(bot))
