from discord.ext import commands
from discord import Option
import sqlite3

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def replaceBool(lean):
    return "Enable"  if str2bool(lean) else "Disable"

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

def toggle_status(key, guild_id):
    # Get the current status
    c_commands.execute(f'SELECT status FROM "c{guild_id}" WHERE key = ?', (key,))
    current_status = c_commands.fetchone()

    if current_status is not None:
        new_status = not current_status[0]  # Toggle the status
        c_commands.execute(f'''
            UPDATE "c{guild_id}" 
            SET status = ? 
            WHERE key = ?
        ''', (new_status, key))
        conn_commands.commit()  # Commit the changes
        return new_status
    return None  # Return None if the key doesn't exist


class Enable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(description="Toggle key trigger")
    async def toggle(self, ctx, input: Option(str, "Input key(str) to enable", required=True)):
        initcommands(ctx.guild.id)
        status = toggle_status(input, ctx.guild.id)
        if status != None:
            await ctx.respond(f'Togger {input} to ***{status}***')
            return
        await ctx.respond('Key does not exist', ephemeral=True, delete_after=1)

def setup(bot):
    bot.add_cog(Enable(bot))