import disnake
from utils.items import ItemChance
from app.views.profileView import ProfileBuilder


class SelectCase(disnake.ui.StringSelect):
    def __init__(self, count_case, user_id, controller, builder) -> None:
        options = [
            disnake.SelectOption(label='case "Power" - 500 CP', value="0", emoji="<:power:1232610069514817538>"),
            disnake.SelectOption(label='case "Gold Rush" - 500 CP', value="1", emoji="<:goldrush:1232610300134428745>"),
            disnake.SelectOption(label='case "Galactic Secrets" - 500 CP', value="2", emoji="<:gs:1232610593278529537>"),
            disnake.SelectOption(label='case "Hunting" - 500 CP', value="3", emoji="<:gs:1232610593278529537>"),
            disnake.SelectOption(label='case "Toxic" - 500 CP', value="4", emoji="<:gs:1232610593278529537>"),
            disnake.SelectOption(label='case "Verdansk" - 500 CP', value="5", emoji="<:gs:1232610593278529537>")
        ]
        super().__init__(
            placeholder="Select a case:",
            min_values=1,
            max_values=1,
            options=options,
        )
        self.count_case = count_case
        self._controller = controller
        self._user_id = user_id
        self.builder = builder

    async def callback(self, interaction: disnake.Interaction):
        if interaction.user.id == self._user_id:
            coin = await self._controller.get_user_coin(interaction.guild.id, self._user_id)
            if self.values[0] == "0":
                await SelectViewOpenCase(self._controller, coin[0], self._user_id, self.builder, self.count_case).first_case(interaction)
            elif self.values[0] == "1":
                await SelectViewOpenCase(self._controller, coin[0], self._user_id, self.builder, self.count_case).second_case(interaction)
            elif self.values[0] == "2":
                await SelectViewOpenCase(self._controller, coin[0], self._user_id, self.builder, self.count_case).third_case(interaction)
            elif self.values[0] == "3":
                await SelectViewOpenCase(self._controller, coin[0], self._user_id, self.builder, self.count_case).fourth_case(interaction)
            elif self.values[0] == "4":
                await SelectViewOpenCase(self._controller, coin[0], self._user_id, self.builder, self.count_case).fifth_case(interaction)
            elif self.values[0] == "5":
                await SelectViewOpenCase(self._controller, coin[0], self._user_id, self.builder, self.count_case).sixth_case(interaction)
        else:
            embed = disnake.Embed(description="<:error:1222469350930251786> Error: You cannot edit another user's profile.", color=disnake.Color(int("ff3737", 16)))
            await interaction.response.send_message(embed=embed, ephemeral=True)


class SelectCasesDown(disnake.ui.View):
    def __init__(self, interaction, count_case, user_id, controller, builder) -> None:
        super().__init__(timeout=120)

        self.add_item(SelectCase(count_case, user_id, controller, builder))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.gray, custom_id=f"refresh:{interaction.author.id}", label="Back to Profile", emoji="<:profile:1230514676396331018>"))


class SelectViewOpenCase(disnake.ui.View):
    def __init__(self, controller, coin, user_id, builder, count_case) -> None:
        super().__init__(timeout=120)
        self._coin = coin
        self._user_id = user_id
        self.index = 0
        self._controller = controller
        self.builder = builder
        self.ItemChance = ItemChance
        self.profile_builder = ProfileBuilder
        self.count_case = count_case

    @disnake.ui.button(label='Open case', emoji="<:spin:1233725430746452030>", style=disnake.ButtonStyle.green)
    async def spin(self, _, interaction: disnake.Interaction):
        if interaction.user.id == self._user_id:
            if self._coin >= 500:
                if self.index == 1:
                    await interaction.response.defer()
                    item_random = await self.ItemChance.random_item_first_case(interaction, self._controller)
                    if item_random[3] == "coin":
                        self._coin = self._coin - 400
                    elif item_random[3] == "coins":
                        self._coin = self._coin - 300
                    else:
                        self._coin = self._coin - 500
                    await self.builder.create_awards_case(interaction, item_random, self._coin, self)
                elif self.index == 2:
                    await interaction.response.defer()
                    item_random = await self.ItemChance.random_item_second_case(interaction, self._controller)
                    if item_random[3] == "coin":
                        self._coin = self._coin - 400
                    elif item_random[3] == "coins":
                        self._coin = self._coin - 300
                    else:
                        self._coin = self._coin - 500
                    await self.builder.create_awards_case(interaction, item_random, self._coin, self)
                elif self.index == 3:
                    await interaction.response.defer()
                    item_random = await self.ItemChance.random_item_third_case(interaction, self._controller)
                    if item_random[3] == "coin":
                        self._coin = self._coin - 400
                    elif item_random[3] == "coins":
                        self._coin = self._coin - 300
                    else:
                        self._coin = self._coin - 500
                    await self.builder.create_awards_case(interaction, item_random, self._coin, self)
                elif self.index == 4:
                    await interaction.response.defer()
                    self._coin = self._coin - 500
                    item_random = await self.ItemChance.random_item_fourth_case(interaction, self._controller)
                    await self.builder.create_awards_case(interaction, item_random, self._coin, self)
                elif self.index == 5:
                    await interaction.response.defer()
                    self._coin = self._coin - 500
                    item_random = await self.ItemChance.random_item_fifth_case(interaction, self._controller)
                    await self.builder.create_awards_case(interaction, item_random, self._coin, self)
                elif self.index == 6:
                    await interaction.response.defer()
                    self._coin = self._coin - 500
                    item_random = await self.ItemChance.random_item_sixth_case(interaction, self._controller)
                    await self.builder.create_awards_case(interaction, item_random, self._coin, self)
            else:
                embed = disnake.Embed(description=f"<:error:1222469350930251786> Error: not enough coins in your balance. [balance: {self._coin}]", color=disnake.Color(int("ff3737", 16)))
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = disnake.Embed(description="<:error:1222469350930251786> Error: You cannot edit another user's profile.", color=disnake.Color(int("ff3737", 16)))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @disnake.ui.button(label="Back", emoji="<:left:1230514652220493854>")
    async def back(self, _, interaction: disnake.Interaction):
        if interaction.user.id == self._user_id:
            self.stop()
            await interaction.response.defer()
            await self.builder.create_open_case_view(interaction, self.count_case)
            await interaction.edit_original_message(view=SelectCasesDown(interaction, self.count_case, interaction.user.id, self._controller, self.builder))
        else:
            embed = disnake.Embed(description="<:error:1222469350930251786> Error: An error occurred when pressing the button [Back to profile]", color=disnake.Color(int("ff3737", 16)))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    async def first_case(self, interaction):
        self.index = 1
        await self.builder.create_case(interaction, self._coin, self, "power")

    async def second_case(self, interaction: disnake.Interaction):
        self.index = 2
        await self.builder.create_case(interaction, self._coin, self, "gold_rush")

    async def third_case(self, interaction: disnake.Interaction):
        self.index = 3
        await self.builder.create_case(interaction, self._coin, self, "gs")

    async def fourth_case(self, interaction: disnake.Interaction):
        self.index = 4
        await self.builder.create_case(interaction, self._coin, self, "hunting")

    async def fifth_case(self, interaction: disnake.Interaction):
        self.index = 5
        await self.builder.create_case(interaction, self._coin, self, "toxic")

    async def sixth_case(self, interaction: disnake.Interaction):
        self.index = 6
        await self.builder.create_case(interaction, self._coin, self, "verdansk")
