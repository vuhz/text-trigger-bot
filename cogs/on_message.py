import discord
from discord.ext import commands
import sqlite3

def table_exists(table_name):
    c_commands.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", ("c" + str(table_name),))
    return c_commands.fetchone() is not None

def match_primary_key(key, guild_id):
    c_commands.execute(f"SELECT * FROM c{guild_id} WHERE key = '{key}'")
    return c_commands.fetchone()

def increment_use(key, guild_id):
    c_commands.execute(f'UPDATE c{guild_id} SET use_count = use_count + 1 WHERE key = ?', (key,))
    conn_commands.commit()

def initdb():
    global c_commands
    global conn_commands
    conn_commands = sqlite3.connect('keytrigger.db')
    c_commands = conn_commands.cursor()

initdb()

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.author.id == 1074079575480483870:
            return

        if table_exists(message.guild.id):
            content = match_primary_key(message.content, message.guild.id)
            print(content)
            # (key, id, content, active, use_count)
            if content and content[3] == True:
                txt = content[2]
                increment_use(message.content, message.guild.id)
                await message.reply(txt, mention_author = False)

def setup(bot):
    bot.add_cog(OnMessage(bot))
