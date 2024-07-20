from disnake.ext import commands
from app.controllers.guildController import UpdateGuild


class OnGuildProcessing(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self.gl_controller = UpdateGuild()

    @commands.Cog.listener()
    async def on_ready(self):
        print("The on_guild.py file has started working")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            await self.gl_controller.insert_new_guild(guild.id)
        except Exception as error:
            print(f"An error occurred [on_guild_join]: {error}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            await self.gl_controller.delete_guild(guild.id)
        except Exception as error:
            print(f"An error occurred [on_guild_remove]: {error}")


def setup(bot):
    bot.add_cog(OnGuildProcessing(bot))

