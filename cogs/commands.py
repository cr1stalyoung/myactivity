import disnake
from disnake.ext import commands, tasks
from app.controllers.profileController import ProfileGetData
from app.controllers.rankingController import RankingProcessing
from app.views.profileView import ProfileBuilder
from app.views.rankingView import RankingBuilder
from app.ui import rankingUI, settingsUI
from typing import Optional


class MyActivityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.profile_controller = ProfileGetData()
        self.ranking_controller = RankingProcessing()
        self.profile_builder = ProfileBuilder
        self.ranking_builder = RankingBuilder
        self.ui_ranking = rankingUI
        self.faq = settingsUI.FAQDrop

    @commands.Cog.listener()
    async def on_ready(self):
        print("The activity.py file has started working")
        await self.update_top50.start()

    @tasks.loop(seconds=300)
    async def update_top50(self):
        try:
            await self.ranking_controller.update_global_top(self.bot)
        except Exception as _ex:
            print(f"[update_top50] | Error when using the task ➔ {_ex}")

    @commands.slash_command(name="me", description="View information about your own or someone else's profile.")
    async def me(self, interaction: disnake.ApplicationCommandInteraction, member: Optional[disnake.Member] = None):
        try:
            await interaction.response.defer()
            await self.profile_builder.create_image_profile(interaction, self.profile_controller, member)
        except Exception as _ex:
            print(f"[me] | Error when using the slash command ➔ {_ex}")

    @commands.slash_command(name="leaders", description="Show server leaderboard.")
    async def leaders(self, interaction: disnake.ApplicationCommandInteraction,
                      additional_options:  str = commands.Param(description="Additional options for displaying the leaderboard", choices=[
                          "Top members with highest score",
                          "Top members with highest level",
                          "Top members with highest number of sent messages",
                          "Top members with the most hours in the voice channel"
                      ], default="score")):
        try:
            await interaction.response.defer()
            option_leader = {"Top members with highest score": "score", "Top members with highest level": "level", "Top members with highest number of sent messages": "count_msg", "Top members with the most hours in the voice channel": "count_voice"}
            option_leader = option_leader.get(additional_options, "score")
            leaders = await self.ranking_controller.get_leaders(interaction.guild.id, interaction.user.id, option_leader)
            if leaders[0]:
                await self.ui_ranking.ServerLeaders(leaders[0], leaders[1:], interaction.user.id, self.ranking_builder, self.bot).update_message(interaction)
            else:
                await interaction.delete_original_message()
                embed = disnake.Embed(
                    description="<:error:1222469350930251786> Error: You're not in the bot database. Write a message or join the voice room. If issue persists, contact support.",
                    color=disnake.Color(int("ff3737", 16)))
                await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as _ex:
            print(f"[leaders] | Error when using the slash command ➔ {_ex}")

    @commands.slash_command(name="top50", description="Show world ranking leaderboard.")
    async def top50(self, interaction: disnake.ApplicationCommandInteraction):
        try:
            await interaction.response.defer()
            top50 = await self.ranking_controller.get_top50()
            user_top50 = await self.ranking_controller.get_user_top50(interaction.guild.id, interaction.user.id)
            if user_top50:
                await self.ui_ranking.WorldLeaders(user_top50, top50, interaction.user.id, self.ranking_builder).update_message(interaction)
            else:
                await interaction.delete_original_message()
                embed = disnake.Embed(
                    description="<:error:1222469350930251786> Error: You're not in the bot database. Write a message or join the voice room. If issue persists, contact support.",
                    color=disnake.Color(int("ff3737", 16)))
                await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as _ex:
            print(f"[top50] | Error when using the slash command ➔ {_ex}")

    @commands.slash_command(name="help", description="Information about the bot or help.")
    async def help_bot(self, interaction: disnake.ApplicationCommandInteraction):
        try:
            embed = disnake.Embed(
                title="MyActivity | General Information",
                description="**MyActivity is a themed Discord bot for Call of Duty that tracks server activity and enables competition with other servers or members using a ranking system. Engage in text or voice chat to earn SR ranking points and CP coins that allows you to unlock chests and enhance your profile.**\n"
                            "\n**Earning CP [<:cp:1234050162205392927>]**\n"
                            "<a:red_point:1234047580388986880> You earn 1 <:cp:1234050162205392927> for every minute spent on voice channels.\n"
                            "<a:red_point:1234047580388986880> You earn 50 <:cp:1234050162205392927> for every new level.\n"
                            "\n**Bot Usage Commands:**\n"
                            "<a:red_point:1234047580388986880> `/me` - View information about your own or someone else's profile.\n"
                            "<a:red_point:1234047580388986880> `/leaders` - Show server leaderboard.\n"
                            "<a:red_point:1234047580388986880> `/top50` - Show world ranking leaderboard.\n"
                            "<a:red_point:1234047580388986880> `/help` - Information about the bot or help.\n",
                color=disnake.Color(int("ff3737", 16)))
            file_gif = disnake.File('resources/red.gif', filename='red.gif')
            embed.set_image(url='attachment://red.gif')
            await interaction.response.send_message(file=file_gif, embed=embed, view=self.faq(), ephemeral=True)
        except Exception as _ex:
            print(f"[help_bot] | Error when using the slash command ➔ {_ex}")


def setup(bot):
    bot.add_cog(MyActivityCommands(bot))
