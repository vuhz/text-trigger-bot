from discord.ext import commands
import discord, os

if __name__ == "__main__":
    intents = discord.Intents.all()
    intents.members = True
    intents.message_content = True
    activity = discord.Activity(name=':3', type=discord.ActivityType.watching)

    bot = commands.Bot(
        command_prefix=".",
        intents=intents,
        activity=activity,
    )

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename[:-3]}')

    bot.run("MY_TOKEN")
