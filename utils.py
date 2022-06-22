from sqlite3.dbapi2 import DatabaseError
import aiosqlite


async def get_prefix(_bot, message):
    db = await aiosqlite.connect("database.db")
    try:
        async with db.execute("SELECT prefix FROM guilds WHERE guildid = ? ", (message.guild.id)) as cursor:
            async for entry in cursor:
                prefix = entry
                return prefix
    except DatabaseError as e:
        return print(f"[ERROR] {e}\n")
    try:
        await db.close()
    except ValueError:
        pass


