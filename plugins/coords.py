#!/usr/local/bin/python3.7
from discord.ext import commands
import plugins.json
import sqlite3

class OwnerCog:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='coords')
    async def coords(self, ctx, _fname='', _x='', _z='', *, _note='n/a'):

        conn = sqlite3.connect('bot_config/coords.db')
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
            print('.db file already exists')
        if _fname == '':
            c.execute("SELECT * FROM coords")
            await ctx.send(str(c.fetchall()).replace('), (','\n').replace('[','').replace(']','').replace('(','').replace(')',''))
        else:
            print(_fname + ' added')
            c.execute("""INSERT INTO coords VALUES (
                        :f_name,
                        :coord_x,
                        :coord_z,
                        :f_note
                        )""",{'f_name':_fname,'coord_x':_x,'coord_z':_z,'f_note':_note})

            conn.commit()

        conn.close()



def setup(bot):
    bot.add_cog(OwnerCog(bot))
