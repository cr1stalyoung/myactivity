import disnake


# -----------------------------------------
# SelectionGeneral
class SelectionGeneral(disnake.ui.View):
    def __init__(self, value, user_id, guild_id, controller, profile_builder, column_name) -> None:
        super().__init__(timeout=180)
        self._value = sorted(value, key=lambda x: (not x[1]))
        self._index = 1
        self._user_id = user_id
        self._guild_id = guild_id
        self._column_name = column_name
        self._current_value_name = None
        self._controller = controller
        self._profile_builder = profile_builder
        self.update_button_visibility()

    def update_button_visibility(self):
        self.previous.disabled = self._index == 1
        self.next.disabled = self._index == len(self._value) - 1

    @disnake.ui.button(label="Previous", emoji="<:left:1230514652220493854>")
    async def previous(self, _, interaction: disnake.Interaction):
        if self._index > 1 and interaction.user.id == self._user_id and interaction.guild.id == self._guild_id:
            self._index -= 1
            self.update_button_visibility()
            await interaction.response.defer()
            await self.update_message(interaction)
        else:
            embed = disnake.Embed(description="<:error:1222469350930251786> Error: You cannot edit another user's profile.", color=disnake.Color(int("ff3737", 16)))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @disnake.ui.button(label="Next", emoji="<:right:1230514663108907130>")
    async def next(self, _, interaction: disnake.Interaction):
        if self._index < len(self._value) - 1 and interaction.user.id == self._user_id and interaction.guild.id == self._guild_id:
            self._index += 1
            self.update_button_visibility()
            await interaction.response.defer()
            await self.update_message(interaction)
        else:
            embed = disnake.Embed(description="<:error:1222469350930251786> Error: You cannot edit another user's profile.", color=disnake.Color(int("ff3737", 16)))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @disnake.ui.button(label="Select", emoji="<:select:1230514139366031430>")
    async def select(self, _, interaction: disnake.Interaction):
        if interaction.user.id == self._user_id:
            self.stop()
            await interaction.response.defer()
            await self._controller.update_general(self._guild_id, self._user_id, self._column_name, self._current_value_name)
            await self._profile_builder.create_image_profile(interaction, self._controller)
        else:
            embed = disnake.Embed(description="<:error:1222469350930251786> Error: You cannot edit another user's profile.", color=disnake.Color(int("ff3737", 16)))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @disnake.ui.button(label="Back to profile", emoji="<:profile:1230514676396331018>")
    async def back(self, _, interaction: disnake.Interaction):
        if interaction.user.id == self._user_id:
            self.stop()
            await interaction.response.defer()
            await self._profile_builder.create_image_profile(interaction, self._controller)
        else:
            embed = disnake.Embed(description="<:error:1222469350930251786> Error: You cannot edit another user's profile.", color=disnake.Color(int("ff3737", 16)))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    async def update_message(self, interaction: disnake.Interaction):
        start_index = max(0, self._index - 1)
        end_index = min(len(self._value), self._index + 2)
        display_themes = self._value[start_index:end_index]
        previous_theme = (None, None)
        current_theme = (None, None)
        next_theme = (None, None)

        for i, (theme_name, value) in enumerate(display_themes, start=start_index):
            if i == start_index and start_index > 0:
                previous_theme = (theme_name, value)
            elif i == self._index:
                current_theme = (theme_name, value)
                self._current_value_name = theme_name
                self.select.disabled = value is False
            elif i == end_index - 1 and end_index < (len(self._value) + 1):
                next_theme = (theme_name, value)

        if self._column_name == "decal":
            await self._profile_builder.create_image_select(interaction, previous_theme, current_theme, next_theme, self)
        elif self._column_name == "operator":
            await self._profile_builder.create_operator_select(interaction, previous_theme, current_theme, next_theme, self)
        else:
            self.stop()
# -----------------------------------------


# -----------------------------------------
# SelectionCard
class SelectionCard(disnake.ui.View):
    def __init__(self, value, user_id, guild_id, controller, profile_builder) -> None:
        super().__init__(timeout=120)
        self._value = sorted(value, key=lambda x: (not x[1]))
        self._index = 1
        self._user_id = user_id
        self._guild_id = guild_id
        self._current_value_name = None
        self._controller = controller
        self._profile_builder = profile_builder
        self.update_button_visibility()

    def update_button_visibility(self):
        self.previous.disabled = self._index == 1
        self.next.disabled = self._index == len(self._value) - 1

    @disnake.ui.button(label="Previous", emoji="<:left:1230514652220493854>")
    async def previous(self, _, interaction: disnake.Interaction):
        if self._index > 1 and interaction.user.id == self._user_id and interaction.guild.id == self._guild_id:
            self._index -= 1
            self.update_button_visibility()
            await interaction.response.defer()
            await self.update_card(interaction)
        else:
            embed = disnake.Embed(description="<:error:1222469350930251786> Error: You cannot edit another user's profile.", color=disnake.Color(int("ff3737", 16)))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @disnake.ui.button(label="Next", emoji="<:right:1230514663108907130>")
    async def next(self, _, interaction: disnake.Interaction):
        if self._index < len(self._value) - 1 and interaction.user.id == self._user_id and interaction.guild.id == self._guild_id:
            self._index += 1
            self.update_button_visibility()
            await interaction.response.defer()
            await self.update_card(interaction)
        else:
            embed = disnake.Embed(description="<:error:1222469350930251786> Error: You cannot edit another user's profile.", color=disnake.Color(int("ff3737", 16)))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @disnake.ui.button(label="Select", emoji="<:select:1230514139366031430>")
    async def select(self, _, interaction: disnake.Interaction):
        if interaction.user.id == self._user_id:
            self.stop()
            await interaction.response.defer()
            if self._current_value_name == "default":
                await self._controller.update_general(self._guild_id, self._user_id, "card", None)
            else:
                await self._controller.update_general(self._guild_id, self._user_id, "card", self._current_value_name)
            await self._profile_builder.create_image_profile(interaction, self._controller)
        else:
            embed = disnake.Embed(description="<:error:1222469350930251786> Error: You cannot edit another user's profile.", color=disnake.Color(int("ff3737", 16)))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @disnake.ui.button(label="Back to profile", emoji="<:profile:1230514676396331018>")
    async def back(self, _, interaction: disnake.Interaction):
        if interaction.user.id == self._user_id:
            self.stop()
            await interaction.response.defer()
            await self._profile_builder.create_image_profile(interaction, self._controller)
        else:
            embed = disnake.Embed(description="<:error:1222469350930251786> Error: You cannot edit another user's profile.", color=disnake.Color(int("ff3737", 16)))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    async def update_card(self, interaction: disnake.Interaction):
        current_theme_name, current_value = self._value[self._index]
        current_card = (current_theme_name, current_value)
        self._current_value_name = current_theme_name
        self.select.disabled = current_value is False
        await self._profile_builder.create_card_select(interaction, current_card, self)
# -----------------------------------------


# -----------------------------------------
# FAQ
class FAQ(disnake.ui.StringSelect):
    def __init__(self) -> None:
        options = [
            disnake.SelectOption(label='General Information', value="0"),
            disnake.SelectOption(label='Rating', value="1"),
            disnake.SelectOption(label='Cases', value="2"),
            disnake.SelectOption(label='Support', value="3")
        ]
        super().__init__(
            placeholder="Select a section:",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.Interaction):
        if self.values[0] == "0":
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
            await interaction.response.edit_message(file=file_gif, embed=embed)
        elif self.values[0] == "1":
            embed = disnake.Embed(
                title="MyActivity | Rating",
                description="**Get ready to dive into a brand new rating activity system in voice channels. Progress through divisions earning <:sr:1234051294046457908> for activity.**\n"
                            "\n**Earning <:sr:1234051294046457908>**\n"
                            "<a:red_point:1234047580388986880> You earn 4 <:sr:1234051294046457908> for every minute spent in voice channels.\n"
                            "\n**Divisions**\n"
                            "<:bronze:1234056403145064488> Bronze 0 - 899 <:sr:1234051294046457908>\n"
                            "<:silver:1234058871228731404> Silver 900 - 2099 <:sr:1234051294046457908>\n"
                            "<:gold:1234058892162502697> Gold 2100 - 3599 <:sr:1234051294046457908>\n"
                            "<:platinum:1234058914161491968> Platinum 3600 - 5399 <:sr:1234051294046457908>\n"
                            "<:diamond:1234058967227961425> Diamond 5400 - 7499 <:sr:1234051294046457908>\n"
                            "<:crimson:1234058995329662986> Crimson 7500 - 9999 <:sr:1234051294046457908>\n"
                            "<:iridescent:1234059044566863963> Iridescent 10000+ <:sr:1234051294046457908>\n"
                            "<:top:1230512136191479870> World Top 50 10000+ <:sr:1234051294046457908>\n"
                            "\n**Penalty for Every Hour of Absence**\n"
                            "<a:red_point:1234047580388986880> For every one hour of absence in a voice channel, you receive a penalty of <:sr:1234051294046457908> depending on your division.\n"
                            "\n**Division Penalties**\n"
                            "<:bronze:1234056403145064488> Bronze - Minus -0 <:sr:1234051294046457908> per hour\n"
                            "<:silver:1234058871228731404> Silver - Minus -3 <:sr:1234051294046457908> per hour\n"
                            "<:gold:1234058892162502697> Gold - Minus -10 <:sr:1234051294046457908> per hour\n"
                            "<:platinum:1234058914161491968> Platinum - Minus -12 <:sr:1234051294046457908> per hour\n"
                            "<:diamond:1234058967227961425> Diamond - Minus -15 <:sr:1234051294046457908> per hour\n"
                            "<:crimson:1234058995329662986> Crimson - Minus -18 <:sr:1234051294046457908> per hour\n"
                            "<:iridescent:1234059044566863963> Iridescent - Minus -25 <:sr:1234051294046457908> per hour\n"
                            "<:top:1230512136191479870> World Top 50 - Minus [-25 to -150] <:sr:1234051294046457908>\n",
                color=disnake.Color(int("ff3737", 16)))
            file_gif = disnake.File('resources/red.gif', filename='red.gif')
            embed.set_image(url='attachment://red.gif')
            await interaction.response.edit_message(file=file_gif, embed=embed)
        elif self.values[0] == "2":
            embed = disnake.Embed(
                title="MyActivity | Cases",
                description="**The bot has a function of opening cases from which you can get items to decorate your profile, both personal and public.**\n"
                            "\n**Item Drop Rates**\n"
                            "<:common:1234061591088074762> Common item - ~53%.\n"
                            "<:uncommon:1234061607831736350> Uncommon item - ~35%.\n"
                            "<:mythical:1234061638873645147> Mythical item - ~10%.\n"
                            "<:ancient:1234061957649268859> Ancient item - ~0.25%.\n"
                            "<:immortal:1234062100498874428> Ultra Rare item - ~0.01%.\n",
                color=disnake.Color(int("ff3737", 16)))
            file_gif = disnake.File('resources/red.gif', filename='red.gif')
            embed.set_image(url='attachment://red.gif')
            await interaction.response.edit_message(file=file_gif, embed=embed)
        elif self.values[0] == "3":
            embed = disnake.Embed(
                title="MyActivity | Support",
                description="**If you encounter an issue with the bot or if you've noticed/found a bug, you can get assistance or report the problem/bug on Discord. Additionally, on Discord, you can stay updated with the bot's news, latest updates, and status.**\n",
                color=disnake.Color(int("ff3737", 16)))
            file_gif = disnake.File('resources/red.gif', filename='red.gif')
            embed.set_image(url='attachment://red.gif')
            await interaction.response.edit_message(file=file_gif, embed=embed)
# -----------------------------------------


# -----------------------------------------
# CALL FAQ
class FAQDrop(disnake.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=300)
        self.add_item(FAQ())
# -----------------------------------------
