# libs #
from __future__ import annotations
import discord,time,os,hashlib
from discord.ext.commands import has_permissions, MissingPermissions
import discord.ext.commands as dec
from discord.ext import commands,tasks
from cogs.Moderaton import Moderation
from cogs.admin import admin
from cogs.economy import economy
from cogs.general import general
from cogs.mics import Mics 
from cogs.utlis.jsonhandeler import JsonHandeler as jh
from cogs.utlis.funcs import filter_ban_msg, leveling,Rank
from cogs.utlis.global_var_handler import remove_user_from_all_database

# constant #
BOT_BY = "gsdev"

# variables #
bot = dec.Bot(command_prefix = '.',intents = discord.Intents().all())
level_db = jh("database/level.json")

## events ##
@bot.event
async def on_ready(): 
    print("bot in online")

@bot.listen()
async def on_message(message):
    if not message.author.bot:
        await leveling(message,level_db)
        x = filter_ban_msg(message.content)
        if x:
            await message.reply("Use of banned word is prohibeted")
            await message.delete()
            bot.wait_for("message")

@bot.event
async def on_member_join(member):
    if not member.bot:
        if member.name in jh("database/mod.json").fetch_data()["user-data"]["black-list"]["names"]:
            uq_sub_name = "".join(list(hashlib.sha1(str(member.id).encode()).hexdigest())[:7])
            member.edit(nick=f"Moderation nickname {uq_sub_name}")
        else:
            pass

@bot.event
async def on_member_update(before,after):
    if not before.bot:
        if after.name in jh("database/mod.json").fetch_data()["user-data"]["black-list"]["names"]:
            after.edit(nick=before.name)
            await after.send("hey the name {0} is blacklisted in {1} so u cannot keep that name".format(after.name,after.guild))

@bot.event
async def on_member_remove(member):
    if not member.bot:
        remove_user_from_all_database(member)

@bot.command()
async def level_data(ctx:dec.context.Context):
    if ctx.author.id == 558311178972037127:
        n = level_db.get_info()
        embed=discord.Embed(title="File data", description="File name :- *level.json*")
        embed.add_field(name="File size :-", value=str(n["size"])+" bytes", inline=True)
        embed.add_field(name="last accessed by admin at :-", value=time.ctime(n["last_access"]), inline=False)
        embed.add_field(name="last modified by bot at :-", value=time.ctime(n["modified"]), inline=True)
        await ctx.send(embed=embed)


if __name__ == "__main__":
    try:
        #bot.add_cog(admin(bot))
        #bot.add_cog(economy(bot))
        #bot.add_cog(general(bot))
        #bot.add_cog(Moderation(bot))
        bot.add_cog(Mics(bot))
    except Exception as e:
        print(f"{type(e).__name__}: {e}")


bot.run(os.getenv('token'))
    ## future me pls make database for every type linr levelinf etc level = tinydb("level,db")