from disnake.ext import commands
from app.controllers.profileController import UpdateProfileMember


class OnMessageProcessing(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self.msg_controller = UpdateProfileMember()

    @commands.Cog.listener()
    async def on_ready(self):
        print("The on_message.py file has started working")

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author.bot:
                return
            experience, level = await self.msg_controller.update_per_message(message.author.guild.id, message.author.id)
            if experience is None or level is None:
                await self.msg_controller.insert_new_profile(message.author.guild.id, message.author.id)
            else:
                level_up = min(300, int(experience / 500))
                if level < level_up:
                    await self.msg_controller.update_level_profile(message.author.guild.id, message.author.id, level_up)
        except Exception as error:
            print(f"An error occurred [on_message]: >>> {error}")


def setup(bot):
    bot.add_cog(OnMessageProcessing(bot))

