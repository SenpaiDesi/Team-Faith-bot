from sqlite3.dbapi2 import IntegrityError
import discord
from discord.ext import commands
import assets
import utils
from datetime import datetime
import aiosqlite

intents = discord.Intents
intents.all()
bot = commands.Bot(command_prefix=utils.get_prefix, case_insensitive = True, intents = intents)


@bot.event
async def on_guild_join(_guild):
    # we don't need to add the guild if it was already there
    db = await aiosqlite.connect("./database.db")
    for guild in bot.guilds:
        try:
            await db.execute("CREATE TABLE IF NOT EXISTS guilds (guildid INTEGER UNIQUE, prefix VARCHAR)")
            await db.commit()
            await db.execute(f"INSERT INTO guilds VALUES ({_guild.id}, '!TF8 ')")
            await db.commit()
        except IntegrityError:
            print(f"{_guild.id} already exists.\n")
        except ValueError:
            pass
        try:
            await db.close()
        except ValueError:
            pass

@bot.event
# Logging in and selecting the first status for the status cycler to use.
async def on_ready():
    # sanity check, in case the bot was added during downtime
    for guild in bot.guilds:
        await on_guild_join(guild)


@bot.command(name="prefix")
async def prefix(prefix=None):
    db = await aiosqlite.connect("database.db")
    if prefix is not None:
        try:
            await db.execute("DELETE FROM guilds WHERE guildid = ?", (bot.guild.id))
            await db.commit()
            await db.execute("INSERT INTO guilds VALUES (?, ?)", (bot.guild.id, prefix))
            await db.commit()
            await db.close()
        except ValueError:
            pass

        
