import disnake
from disnake.ext import commands
from app.controllers.profileController import ProfileGetData
from app.controllers.casesController import Cases
from app.views.profileView import ProfileBuilder
from app.views.casesView import CasesBuilder
from app.ui import settingsUI
from app.ui import casesUI


class ProcessingOnButtonClick(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self.profile_controller = ProfileGetData()
        self.profile_builder = ProfileBuilder()
        self.cases_controller = Cases()
        self.cases_builder = CasesBuilder
        self.selection_general = settingsUI
        self.cases_ui = casesUI

    @commands.Cog.listener()
    async def on_ready(self):
        print("The buttons.py file has started working")

    @commands.Cog.listener()
    async def on_button_click(self, interaction: disnake.MessageInteraction):
        split_user_id = interaction.user.id == int(interaction.component.custom_id.split(":")[1]) if ":" in interaction.component.custom_id else False
        error_message = "<:error:1222469350930251786> Error: You cannot edit another user's profile."

        if interaction.component.custom_id.startswith("refresh"):
            if split_user_id:
                await interaction.response.defer()
                await self.profile_builder.create_image_profile(interaction, self.profile_controller)
            else:
                embed = disnake.Embed(description=error_message, color=disnake.Color(int("ff3737", 16)))
                await interaction.response.send_message(embed=embed, ephemeral=True)
        elif interaction.component.custom_id.startswith("settings"):
            if split_user_id:
                decal = disnake.ui.Button(style=disnake.ButtonStyle.gray, custom_id=f"decal:{interaction.author.id}", label="Theme", emoji="<:theme:1230521151424299019>")
                card = disnake.ui.Button(style=disnake.ButtonStyle.gray, custom_id=f"operator:{interaction.author.id}", label="Operator", emoji="<:operator:1230518490956566558>")
                operator = disnake.ui.Button(style=disnake.ButtonStyle.gray, custom_id=f"card:{interaction.author.id}", label="Card", emoji="<:card:1230520578507804702>")
                back = disnake.ui.Button(style=disnake.ButtonStyle.gray, custom_id=f"back:{interaction.author.id}", label="Back", emoji="<:profile:1230514676396331018>")
                await interaction.response.edit_message(components=[decal, card, operator, back])
            else:
                embed = disnake.Embed(description=error_message, color=disnake.Color(int("ff3737", 16)))
                await interaction.response.send_message(embed=embed, ephemeral=True)
        elif interaction.component.custom_id.startswith("faq"):
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
            await interaction.response.send_message(file=file_gif, embed=embed, view=self.selection_general.FAQDrop(), ephemeral=True)
        elif interaction.component.custom_id.startswith("case"):
            if split_user_id:
                await interaction.response.defer()
                guild = await self.cases_controller.get_guild(interaction.guild.id)
                if guild is None:
                    await self.cases_controller.insert_new_guild(interaction.guild.id)
                cases = await self.cases_controller.get_count_cases(interaction.guild.id)
                await self.cases_builder.create_open_case_view(interaction, cases)
                await interaction.edit_original_message(view=self.cases_ui.SelectCasesDown(interaction, cases, interaction.user.id, self.cases_controller, self.cases_builder))
            else:
                embed = disnake.Embed(description=error_message, color=disnake.Color(int("ff3737", 16)))
                await interaction.response.send_message(embed=embed, ephemeral=True)
        elif interaction.component.custom_id.startswith("decal"):
            await interaction.response.defer()
            if split_user_id:
                theme = await self.profile_controller.get_decals(interaction.guild.id, interaction.user.id)
                await self.selection_general.SelectionGeneral(theme, interaction.user.id, interaction.guild.id, self.profile_controller, self.profile_builder, "decal").update_message(interaction)
            else:
                embed = disnake.Embed(description=error_message, color=disnake.Color(int("ff3737", 16)))
                await interaction.response.send_message(embed=embed, ephemeral=True)
        elif interaction.component.custom_id.startswith("operator"):
            await interaction.response.defer()
            if split_user_id:
                operator = await self.profile_controller.get_operators(interaction.guild.id, interaction.user.id)
                await self.selection_general.SelectionGeneral(operator, interaction.user.id, interaction.guild.id, self.profile_controller, self.profile_builder, "operator").update_message(interaction)
            else:
                embed = disnake.Embed(description=error_message, color=disnake.Color(int("ff3737", 16)))
                await interaction.response.send_message(embed=embed, ephemeral=True)
        elif interaction.component.custom_id.startswith("card"):
            await interaction.response.defer()
            if split_user_id:
                card = await self.profile_controller.get_cards(interaction.guild.id, interaction.user.id)
                card.insert(1, ("default", True))
                await self.selection_general.SelectionCard(card, interaction.user.id, interaction.guild.id, self.profile_controller, self.profile_builder).update_card(interaction)
            else:
                embed = disnake.Embed(description=error_message, color=disnake.Color(int("ff3737", 16)))
                await interaction.response.send_message(embed=embed, ephemeral=True)
        elif interaction.component.custom_id.startswith("back"):
            if split_user_id:
                await interaction.response.defer()
                settings = disnake.ui.Button(style=disnake.ButtonStyle.gray, custom_id=f"settings:{interaction.author.id}", label="Settings", emoji="<:settings:1230512055820226631>")
                refresh = disnake.ui.Button(style=disnake.ButtonStyle.gray, custom_id=f"refresh:{interaction.author.id}", label="Refresh", emoji="<:refresh:1230512089978638337>")
                faq = disnake.ui.Button(style=disnake.ButtonStyle.gray, custom_id=f"faq:{interaction.author.id}", label="FAQ", emoji="<:faq:1230512113596764191>")
                case = disnake.ui.Button(style=disnake.ButtonStyle.gray, custom_id=f"case:{interaction.author.id}", label="Cases", emoji="<:case:1230512170182377563>")
                invite = disnake.ui.Button(style=disnake.ButtonStyle.gray, label="Get CP", url="https://discord.gg/wXKCr8WKUt", emoji="<:cp:1234050162205392927>")
                await interaction.edit_original_message(components=[settings, refresh, faq, case, invite])
            else:
                embed = disnake.Embed(description=error_message, color=disnake.Color(int("ff3737", 16)))
                await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(ProcessingOnButtonClick(bot))
