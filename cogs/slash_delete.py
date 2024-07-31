import discord, re
from discord.ext import commands
from discord import Option
import sqlite3

bot = discord.Bot()

def findEmo(message):
    #input: .emoji.emojiID or a.emoji.emojiID for animated emoji
    p1 = re.search(pattern=r'a\.[a-zA-Z0-9]+\.\d+', string=message)
    p2 = re.search(pattern=r'\.[a-zA-Z0-9]+\.\d+', string=message)
    emoji = p1 if p1 else p2
    return message.replace(emoji.group(0), f'<{emoji.group(0).replace(".", ":")}>' ) if emoji else message

def initcommands(id):
    global c_commands
    global conn_commands
    conn_commands = sqlite3.connect('keytrigger.db')
    c_commands = conn_commands.cursor()
    c_commands.execute(f'''
    CREATE TABLE IF NOT EXISTS "c{id}" (
        key TEXT PRIMARY KEY,
        id INTEGER,
        value TEXT,
        status BOOLEAN,
        use_count INTEGER
    )
    ''')

def delete_row(key, guild_id):
    c_commands.execute(f'DELETE FROM "c{guild_id}" WHERE key = ?', (key,))
    conn_commands.commit()  

def check_legit(key, guild_id, user_id):
    c_commands.execute(f'SELECT * FROM "c{guild_id}" WHERE key = ?', (key,))
    a = c_commands.fetchone()
    return a and user_id == a[1]

class Delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(description="Delete custom command (require user is command's author, or super secret key :d)")
    async def delete(self, ctx, input: Option(str, "Input key(str) to delete", required=True)):
        initcommands(ctx.guild.id)
        if not check_legit(findEmo(input), ctx.guild.id, ctx.author.id):
            await ctx.respond(f'Key not exist!', ephemeral=True, delete_after=3)
            return
        
        delete_row(findEmo(input), ctx.guild.id)
        await ctx.respond(f'Deleted {input}', ephemeral=True, delete_after=3)


def setup(bot):
    bot.add_cog(Delete(bot))