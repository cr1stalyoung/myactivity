from disnake.ext import commands
from datetime import datetime
from app.controllers.profileController import UpdateProfileMember
from utils.division import Division


class OnVoiceProcessing(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self.vc_controller = UpdateProfileMember()
        self.division = Division()

    @commands.Cog.listener()
    async def on_ready(self):
        print("The on_voice_state_update.py file has started working")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            if member.bot:
                return
            if before.channel is None or before.self_mute:
                last_entry, score = await self.vc_controller.get_member_data(member.guild.id, member.id)
                if last_entry is None or score is None:
                    await self.vc_controller.insert_new_profile(member.guild.id, member.id)
                else:
                    get_score_per_hour = int((datetime.utcnow() - datetime.fromisoformat(str(last_entry))).total_seconds() / 3600)
                    if get_score_per_hour != 0:
                        minus = await self.division.minus(score)
                        new_score = max(0, score - (get_score_per_hour * minus))
                        await self.vc_controller.update_member_before(member.guild.id, member.id, datetime.utcnow(), new_score)
                    else:
                        await self.vc_controller.update_member_time(member.guild.id, member.id, datetime.utcnow())
            elif after.channel is None or after.self_mute:
                last_entry, _ = await self.vc_controller.get_member_data(member.guild.id, member.id)
                if last_entry is None:
                    await self.vc_controller.insert_new_profile(member.guild.id, member.id)
                else:
                    data_per_minute = int((datetime.utcnow() - datetime.fromisoformat(str(last_entry))).total_seconds() / 60)
                    if data_per_minute != 0:
                        experience, level, longest = await self.vc_controller.update_member_after(member.guild.id, member.id, data_per_minute, min(1600, data_per_minute * 4))
                        if longest < data_per_minute:
                            await self.vc_controller.update_member_longest(member.guild.id, member.id, data_per_minute)
                        level_up = min(300, int(experience / 500))
                        if level < level_up:
                            await self.vc_controller.update_level_profile(member.guild.id, member.id, level_up)
        except Exception as error:
            print(f"An error occurred [on_voice_state_update]: {error}")


def setup(bot):
    bot.add_cog(OnVoiceProcessing(bot))

