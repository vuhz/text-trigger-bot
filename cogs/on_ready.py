from discord.ext import commands

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logging as {self.bot.user}!')
        await self.bot.register_commands()

def setup(bot):
    bot.add_cog(OnReady(bot))