import disnake


class ServerLeaders(disnake.ui.View):
    def __init__(self, user_data, top_data, user_id, ranking_builder, bot) -> None:
        super().__init__(timeout=120)
        self._user_data = user_data
        self._top_data = top_data
        self._user_id = user_id
        self._ranking_builder = ranking_builder
        self._bot = bot
        self.index = 1
        self.update_button_visibility()

    def update_button_visibility(self):
        self.previous.disabled = self.index == 1
        self.next.disabled = len(self._top_data) <= 10 or self.index >= len(self._top_data) - 9

    @disnake.ui.button(label="Previous", emoji="<:left:1230514652220493854>")
    async def previous(self, _, interaction: disnake.Interaction):
        if self.index > 10 and interaction.user.id == self._user_id:
            self.index -= 10
            self.update_button_visibility()
            await interaction.response.defer()
            await self.update_message(interaction)
        else:
            embed = disnake.Embed(description="<:error:1222469350930251786> Error: An error occurred when pressing the button [Previous]", color=disnake.Color(int("ff3737", 16)))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @disnake.ui.button(label="Next", emoji="<:right:1230514663108907130>")
    async def next(self, _, interaction: disnake.Interaction):
        if self.index < len(self._top_data) - 10 and interaction.user.id == self._user_id:
            self.index += 10
            self.update_button_visibility()
            await interaction.response.defer()
            await self.update_message(interaction)
        else:
            embed = disnake.Embed(description="<:error:1222469350930251786> Error: An error occurred when pressing the button [Next]", color=disnake.Color(int("ff3737", 16)))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @disnake.ui.button(label="Exit", emoji="<:exit:1236391967110467735>")
    async def back(self, _, interaction: disnake.Interaction):
        if interaction.user.id == self._user_id:
            self.stop()
            await interaction.response.defer()
            await interaction.delete_original_message()
        else:
            embed = disnake.Embed(description="<:error:1222469350930251786> Error: An error occurred when pressing the button [Exit]", color=disnake.Color(int("ff3737", 16)))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    async def update_message(self, interaction: disnake.Interaction):
        top_data = self._top_data[self.index - 1:self.index + 9]
        await self._ranking_builder.create_image_server(interaction, self._user_data, top_data, self._bot, self)


class WorldLeaders(disnake.ui.View):
    def __init__(self, user_data, top_data, user_id, ranking_builder) -> None:
        super().__init__(timeout=120)
        self._user_data = user_data
        self._top_data = top_data
        self._user_id = user_id
        self._ranking_builder = ranking_builder
        self._index = 1
        self.update_button_visibility()

    def update_button_visibility(self):
        self.previous.disabled = self._index == 1
        self.next.disabled = self._index == len(self._top_data) - 9

    @disnake.ui.button(label="Previous", emoji="<:left:1230514652220493854>")
    async def previous(self, _, interaction: disnake.Interaction):
        if self._index > 10 and interaction.user.id == self._user_id:
            self._index -= 10
            self.update_button_visibility()
            await interaction.response.defer()
            await self.update_message(interaction)
        else:
            embed = disnake.Embed(description="<:error:1222469350930251786> Error: An error occurred when pressing the button [Previous]", color=disnake.Color(int("ff3737", 16)))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @disnake.ui.button(label="Next", emoji="<:right:1230514663108907130>")
    async def next(self, _, interaction: disnake.Interaction):
        if self._index < len(self._top_data) - 10 and interaction.user.id == self._user_id:
            self._index += 10
            self.update_button_visibility()
            await interaction.response.defer()
            await self.update_message(interaction)
        else:
            embed = disnake.Embed(description="<:error:1222469350930251786> Error: An error occurred when pressing the button [Next]", color=disnake.Color(int("ff3737", 16)))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @disnake.ui.button(label="Exit", emoji="<:exit:1236391967110467735>")
    async def back(self, _, interaction: disnake.Interaction):
        if interaction.user.id == self._user_id:
            self.stop()
            await interaction.response.defer()
            await interaction.delete_original_message()
        else:
            embed = disnake.Embed(description="<:error:1222469350930251786> Error: An error occurred when pressing the button [Exit]", color=disnake.Color(int("ff3737", 16)))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    async def update_message(self, interaction: disnake.Interaction):
        top_data = self._top_data[self._index - 1:self._index + 9]
        await self._ranking_builder.create_image_global(interaction, self._user_data, top_data, self)