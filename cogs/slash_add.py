import discord,re
from discord.ext import commands
from discord import Option
import sqlite3

bot = discord.Bot()

def findEmo(message):
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

def check_legit(key, guild_id, user_id):
    c_commands.execute(f'SELECT * FROM "c{guild_id}" WHERE key = ?', (key,))
    a = c_commands.fetchone()
    return a and user_id == a[1]

class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(description='Message trigger')
    async def add(self, ctx,input: Option(str, "Text to trigger", required=True),
                   message: Option(str, "Message (could be text, link, ping role or sth)",
                   required=True)):
        initcommands(ctx.guild.id)
        xd = f'''
        INSERT OR REPLACE INTO "c{ctx.guild.id}" (key, id, value, status, use_count) 
        VALUES (?, ?, ?, ?, ?)
        '''
        if check_legit(findEmo(input), ctx.guild.id, ctx.author.id):
            await ctx.respond('Key exist!', ephemeral=True, delete_after=5)
            return
        try:
            c_commands.execute(xd, (findEmo(input), ctx.author.id, findEmo(message), True, 0))
            conn_commands.commit()  
            await ctx.respond(f'Added {input}', ephemeral=True, delete_after=1)
        except Exception as e:
            print(f"Error inserting data: {e}")
            await ctx.respond('Failed to add the trigger.', ephemeral=True, delete_after=5)

def setup(bot):
    bot.add_cog(Add(bot))