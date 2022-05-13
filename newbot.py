# libs #
from __future__ import annotations
import discord,time,os,hashlib
from discord.ext.commands import has_permissions, MissingPermissions
import discord.ext.commands as dec
from cogs.mics import Mics 
from cogs.utlis.jsonhandeler import JsonHandeler as jh

# constant #
BOT_BY = "gsdev"

# variables #
bot = dec.Bot(command_prefix = '.',intents = discord.Intents().all())

## events ##
@bot.event
async def on_ready(): 
    print("bot in online")

if __name__ == "__main__":
    try:
        bot.add_cog(Mics(bot))
    except Exception as e:
        print(f"{type(e).__name__}: {e}")

@bot.command()
async def colors(ctx):
    await ctx.send("For place we use hex colors \n for online converter use \n https://www.color-hex.com/")
bot.run(os.getenv('token'))
    ## future me pls make database for every type linr levelinf etc level = tinydb("level,db")
