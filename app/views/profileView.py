import io
import disnake
from PIL import Image, ImageDraw, ImageFont
from utils.division import Division
from utils.prestige import Level
from utils.pillow import PIL


class ProfileBuilder:
    _division = Division
    _pil = PIL
    _level = Level

    @classmethod
    async def create_image_profile(cls, interaction, profile, member=None):
        if member is None:
            user_data = await profile.get_profile(interaction.guild.id, interaction.user.id)
            if user_data is not None:
                # -----------------------------------------
                # Variables
                truncated_name = interaction.user.name.upper()
                truncated_guild_name = interaction.guild.name.upper()
                create_date = interaction.author.created_at.strftime("%d/%m/%Y")
                join_date = interaction.author.joined_at.strftime("%d/%m/%Y")
                agencyfb_bold = "resources/fonts/agencyfb_bold.ttf"
                calibri_bold = "resources/fonts/calibri_bold.ttf"
                user_avatar_url = interaction.user.avatar.url if interaction.user.avatar else "https://img.icons8.com/external-justicon-flat-justicon/1x/external-discord-social-media-justicon-flat-justicon.png"
                guild_avatar_url = interaction.guild.icon.url if interaction.guild.icon else "https://img.icons8.com/external-justicon-flat-justicon/1x/external-discord-social-media-justicon-flat-justicon.png"
                background = Image.open(f"resources/theme/{user_data['decal']}.jpg")
                draw = ImageDraw.Draw(background)
                # -----------------------------------------

                # -----------------------------------------
                # User Information Box
                draw.text((103, 238), f"{create_date}", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=26))
                draw.text((252, 238), f"{join_date}", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=26))
                draw.text((237, 80), f"{truncated_name}", color="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=32))
                draw.text((275, 115), f"{truncated_guild_name}", color="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=28))
                draw.text((272, 188), f"{user_data['pos_server']}", color="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=28))

                avatar = await cls._pil.load_async_image(user_avatar_url)
                avatar = await cls._pil.rounded_corners(avatar, 25)
                avatar = avatar.resize((130, 130))
                background.paste(avatar, (96, 78), avatar.split()[3])

                avatar_guild = await cls._pil.load_async_image(guild_avatar_url)
                guild_avatar = avatar_guild.resize((30, 30))
                background.paste(guild_avatar, (237, 112))

                frame = Image.open("resources/icon/frame.png")
                background.paste(frame, (96, 78), frame.split()[3])
                # -----------------------------------------

                # -----------------------------------------
                # Rating Box
                rank = user_data['pos_world']
                score = user_data['score']
                if score >= 10000:
                    if rank == 1:
                        top1 = Image.open("resources/rank/top1.png")
                        background.paste(top1, (83, 274), top1.split()[3])
                        draw.text((300, 370), f"{score}", fill="white", font=ImageFont.truetype(agencyfb_bold, size=31))
                    elif 1 < rank <= 50:
                        top50 = Image.open("resources/rank/top50.png")
                        background.paste(top50, (83, 274), top50.split()[3])
                        draw.text((300, 370), f"{score}", fill="white", font=ImageFont.truetype(agencyfb_bold, size=31))
                        if rank <= 9:
                            await cls._pil.draw_text_with_outline(draw, (155, 372), f"{rank}", ImageFont.truetype(calibri_bold, size=33), "black", "#e1e1e1", 1)
                        else:
                            await cls._pil.draw_text_with_outline(draw, (148, 373), f"{rank}", ImageFont.truetype(calibri_bold, size=29), "black", "#e1e1e1", 1)
                    else:
                        iridescent = Image.open("resources/rank/iridescent.png")
                        background.paste(iridescent, (83, 274), iridescent.split()[3])
                        draw.text((300, 370), f"{score}", fill="white", font=ImageFont.truetype(agencyfb_bold, size=31))
                else:
                    sr, division = await cls._division.definition(score)
                    img_division = Image.open(division[0])
                    filled_width = int(126 * ((score - sr[0]) / (sr[1] - sr[0])))
                    background.paste(img_division, (83, 274), img_division.split()[3])
                    draw.text((310, 320), f"{score}", fill="white", font=ImageFont.truetype(agencyfb_bold, size=30))
                    draw.rectangle([253, 386, 253 + 126, 386 + 3], fill=division[1])
                    draw.rectangle([253, 386, 253 + filled_width, 386 + 3], fill="#c7a429")
                # -----------------------------------------

                # -----------------------------------------
                # Progress Box
                bar_percentage = (user_data['experience'] % 500) / 500
                draw.arc((148, 444, 332, 626), start=-90, end=(-90+int(360*bar_percentage)), fill="#e1e1e1", width=13)
                bar_percentage = int(bar_percentage * 100)
                if 10 > bar_percentage >= 0:
                    draw.text((222, 521), f"{bar_percentage}%", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=36))
                else:
                    draw.text((213, 520), f"{bar_percentage}%", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=36))
                # -----------------------------------------

                # -----------------------------------------
                # Level box
                level = user_data['level']
                name_card = user_data['card']
                prestige_image = await cls._level.get_image(level)
                prestige = Image.open(f"resources/level/{prestige_image[0]}")
                bar_level = Image.open("resources/icon/bar_level.png")
                background.paste(prestige, (416, 170), prestige.split()[3])
                background.paste(bar_level, (425, 238), bar_level.split()[3])
                await cls._pil.draw_text_with_outline(draw, (prestige_image[1], 242), f"{level}", ImageFont.truetype(calibri_bold, size=26), "#e1e1e1", "#262626", 1)
                if name_card is not None:
                    card = Image.open(f"resources/card/{name_card}.png")
                    background.paste(card, (515, 163), card.split()[3])
                # -----------------------------------------

                # -----------------------------------------
                # Boxing with achievement
                if user_data['season_one'] is not None:
                    achievement = Image.open(f"resources/icon/{user_data['season_one']}.png")
                    background.paste(achievement, (407, 284), achievement.split()[3])
                # -----------------------------------------

                # -----------------------------------------
                # Operator Box
                operators = Image.open(f"resources/operators/{user_data['operator']}.png")
                background.paste(operators, (0, 0), operators.split()[3])
                # -----------------------------------------

                # -----------------------------------------
                # Statistics box
                # voice activity
                draw.text((572, 435), f"{int(user_data['count_voice'] / 60)} h.", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=25))
                # chat activity
                draw.text((565, 477), f"{user_data['count_msg']} m.", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=25))
                # longest time in voice channel
                draw.text((715, 519), f"{int(user_data['longest'] / 60)} h.", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=25))
                # Voice activity per month
                draw.text((669, 559), f"{int(user_data['voice_month'] / 60)} h.", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=25))
                # total rating change per month
                draw.text((721, 600), f"{user_data['score_month']} SR", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=25))
                # -----------------------------------------

                # -----------------------------------------
                # Message creation and sending
                image_bytes = io.BytesIO()
                background.save(image_bytes, format="JPEG")
                image_bytes.seek(0)
                file = disnake.File(fp=image_bytes, filename="warzone.jpg")
                settings = disnake.ui.Button(style=disnake.ButtonStyle.gray, custom_id=f"settings:{interaction.author.id}", label="Settings", emoji="<:settings:1230512055820226631>")
                refresh = disnake.ui.Button(style=disnake.ButtonStyle.gray, custom_id=f"refresh:{interaction.author.id}", label="Refresh", emoji="<:refresh:1230512089978638337>")
                faq = disnake.ui.Button(style=disnake.ButtonStyle.gray, custom_id=f"faq:{interaction.author.id}", label="FAQ", emoji="<:faq:1230512113596764191>")
                case = disnake.ui.Button(style=disnake.ButtonStyle.gray, custom_id=f"case:{interaction.author.id}", label="Cases", emoji="<:case:1230512170182377563>")
                invite = disnake.ui.Button(style=disnake.ButtonStyle.gray, label="Get CP", url="https://discord.gg/wXKCr8WKUt", emoji="<:cp:1234050162205392927>")
                await interaction.edit_original_message(file=file, attachments=None)
                await interaction.edit_original_message(components=[settings, refresh, faq, case, invite])
                # -----------------------------------------
            else:
                await interaction.delete_original_message()
                embed = disnake.Embed(
                    description="<:error:1222469350930251786> Error: You're not in the bot database. Write a message or join friend's voice room. If issue persists, contact support.",
                    color=disnake.Color(int("ff3737", 16)))
                await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            member_data = await profile.get_profile(member.guild.id, member.id)
            if member_data is not None:
                # -----------------------------------------
                # Variables
                truncated_name = member.name.upper()
                truncated_guild_name = member.guild.name.upper()
                create_date = member.created_at.strftime("%d/%m/%Y")
                join_date = member.joined_at.strftime("%d/%m/%Y")
                agencyfb_bold = "resources/fonts/agencyfb_bold.ttf"
                calibri_bold = "resources/fonts/calibri_bold.ttf"
                user_avatar_url = member.avatar.url if member.avatar else "https://img.icons8.com/external-justicon-flat-justicon/1x/external-discord-social-media-justicon-flat-justicon.png"
                guild_avatar_url = member.guild.icon.url if member.guild.icon else "https://img.icons8.com/external-justicon-flat-justicon/1x/external-discord-social-media-justicon-flat-justicon.png"
                background = Image.open(f"resources/theme/{member_data['decal']}.jpg")
                draw = ImageDraw.Draw(background)
                # -----------------------------------------

                # -----------------------------------------
                # User Information Box
                draw.text((103, 238), f"{create_date}", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=26))
                draw.text((252, 238), f"{join_date}", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=26))
                draw.text((237, 80), f"{truncated_name}", color="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=32))
                draw.text((275, 115), f"{truncated_guild_name}", color="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=28))
                draw.text((272, 188), f"{member_data['pos_server']}", color="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=28))

                avatar = await cls._pil.load_async_image(user_avatar_url)
                avatar = await cls._pil.rounded_corners(avatar, 25)
                avatar = avatar.resize((130, 130))
                background.paste(avatar, (96, 78), avatar.split()[3])

                avatar_guild = await cls._pil.load_async_image(guild_avatar_url)
                guild_avatar = avatar_guild.resize((30, 30))
                background.paste(guild_avatar, (237, 112))

                frame = Image.open("resources/icon/frame.png")
                background.paste(frame, (96, 78), frame.split()[3])
                # -----------------------------------------

                # -----------------------------------------
                # Rating Box
                rank = member_data['pos_world']
                score = member_data['score']
                if score >= 10000:
                    if rank == 1:
                        top1 = Image.open("resources/rank/top1.png")
                        background.paste(top1, (83, 274), top1.split()[3])
                        draw.text((300, 370), f"{score}", fill="white", font=ImageFont.truetype(agencyfb_bold, size=31))
                    elif 1 < rank <= 50:
                        top50 = Image.open("resources/rank/top50.png")
                        background.paste(top50, (83, 274), top50.split()[3])
                        draw.text((300, 370), f"{score}", fill="white", font=ImageFont.truetype(agencyfb_bold, size=31))
                        if rank <= 9:
                            await cls._pil.draw_text_with_outline(draw, (155, 372), f"{rank}", ImageFont.truetype(calibri_bold, size=33), "black", "#e1e1e1", 1)
                        else:
                            await cls._pil.draw_text_with_outline(draw, (148, 373), f"{rank}", ImageFont.truetype(calibri_bold, size=29), "black", "#e1e1e1", 1)
                    else:
                        iridescent = Image.open("resources/rank/iridescent.png")
                        background.paste(iridescent, (83, 274), iridescent.split()[3])
                        draw.text((300, 370), f"{score}", fill="white", font=ImageFont.truetype(agencyfb_bold, size=31))
                else:
                    sr, division = await cls._division.definition(score)
                    img_division = Image.open(division[0])
                    filled_width = int(126 * ((score - sr[0]) / (sr[1] - sr[0])))
                    background.paste(img_division, (83, 274), img_division.split()[3])
                    draw.text((310, 320), f"{score}", fill="white", font=ImageFont.truetype(agencyfb_bold, size=30))
                    draw.rectangle([253, 386, 253 + 126, 386 + 3], fill=division[1])
                    draw.rectangle([253, 386, 253 + filled_width, 386 + 3], fill="#c7a429")
                # -----------------------------------------

                # -----------------------------------------
                # Progress Box
                bar_percentage = (member_data['experience'] % 500) / 500
                draw.arc((148, 444, 332, 626), start=-90, end=(-90+int(360*bar_percentage)), fill="#e1e1e1", width=13)
                bar_percentage = int(bar_percentage * 100)
                if 10 > bar_percentage >= 0:
                    draw.text((222, 521), f"{bar_percentage}%", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=36))
                else:
                    draw.text((213, 520), f"{bar_percentage}%", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=36))
                # -----------------------------------------

                # -----------------------------------------
                # Level box
                level = member_data['level']
                name_card = member_data['card']
                prestige_image = await cls._level.get_image(level)
                prestige = Image.open(f"resources/level/{prestige_image[0]}")
                bar_level = Image.open("resources/icon/bar_level.png")
                background.paste(prestige, (416, 170), prestige.split()[3])
                background.paste(bar_level, (425, 238), bar_level.split()[3])
                await cls._pil.draw_text_with_outline(draw, (prestige_image[1], 242), f"{level}", ImageFont.truetype(calibri_bold, size=26), "#e1e1e1", "#262626", 1)
                if name_card is not None:
                    card = Image.open(f"resources/card/{name_card}.png")
                    background.paste(card, (515, 163), card.split()[3])
                # -----------------------------------------

                # -----------------------------------------
                # Boxing with achievement
                if member_data['season_one'] is not None:
                    achievement = Image.open(f"resources/icon/{member_data['season_one']}.png")
                    background.paste(achievement, (407, 284), achievement.split()[3])
                # -----------------------------------------

                # -----------------------------------------
                # Operator Box
                operators = Image.open(f"resources/operators/{member_data['operator']}.png")
                background.paste(operators, (0, 0), operators.split()[3])
                # -----------------------------------------

                # -----------------------------------------
                # Statistics box
                # voice activity
                draw.text((572, 435), f"{int(member_data['count_voice'] / 60)} h.", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=25))
                # chat activity
                draw.text((565, 477), f"{member_data['count_msg']} m.", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=25))
                # longest time in voice channel
                draw.text((715, 519), f"{int(member_data['longest'] / 60)} h.", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=25))
                # Voice activity per month
                draw.text((669, 559), f"{int(member_data['voice_month'] / 60)} h.", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=25))
                # total rating change per month
                draw.text((721, 600), f"{member_data['score_month']} SR", fill="#e1e1e1", font=ImageFont.truetype(calibri_bold, size=25))
                # -----------------------------------------

                # -----------------------------------------
                # Message creation and sending
                image_bytes = io.BytesIO()
                background.save(image_bytes, format="JPEG")
                image_bytes.seek(0)
                file = disnake.File(fp=image_bytes, filename="warzone.jpg")
                await interaction.edit_original_message(file=file, attachments=None)
                # -----------------------------------------
            else:
                await interaction.delete_original_message()
                embed = disnake.Embed(
                    description="<:error:1222469350930251786> Error: Member not found in the bot database. If the issue persists, contact support.",
                    color=disnake.Color(int("ff3737", 16)))
                await interaction.followup.send(embed=embed, ephemeral=True)

    @staticmethod
    async def create_image_select(interaction, prev, current, next, view):
        # -----------------------------------------
        # Open files
        background = Image.open("resources/theme/select/select.jpg")
        add_frame = Image.open("resources/theme/select/addframe.png")
        current_frame = Image.open("resources/theme/select/currentframe.png")
        prev_close = Image.open("resources/theme/select/prev_close.png").resize((453, 303))
        next_close = Image.open("resources/theme/select/next_close.png").resize((453, 303))
        current_close = Image.open("resources/theme/select/current_close.png").resize((607, 405))
        black = Image.open("resources/theme/select/black.png").resize((453, 303))
        # -----------------------------------------

        # -----------------------------------------
        # Display previous values
        if prev[0] is not None:
            background.paste(add_frame, (12, 252), add_frame.split()[3])
            background.paste(Image.open(f"resources/theme/{prev[0]}.jpg").resize((453, 303)), (38, 258))
            if prev[1] is False:
                background.paste(prev_close, (38, 258), prev_close.split()[3])
            else:
                background.paste(black, (38, 258), black.split()[3])
        # -----------------------------------------

        # -----------------------------------------
        # Display next values
        if next[0] is not None:
            background.paste(add_frame, (690, 252), add_frame)
            background.paste(Image.open(f"resources/theme/{next[0]}.jpg").resize((453, 303)), (715, 258))
            if next[1] is False:
                background.paste(next_close, (715, 258), next_close.split()[3])
            else:
                background.paste(black, (715, 258), black.split()[3])
        # -----------------------------------------

        # -----------------------------------------
        # Display current values
        background.paste(current_frame, (264, 206), current_frame.split()[3])
        background.paste(Image.open(f"resources/theme/{current[0]}.jpg").resize((607, 405)), (297, 212))
        if current[1] is False:
            background.paste(current_close, (297, 212), current_close.split()[3])
        # -----------------------------------------

        # -----------------------------------------
        # Message creation and sending
        image_bytes = io.BytesIO()
        background.save(image_bytes, format="JPEG")
        image_bytes.seek(0)
        file = disnake.File(fp=image_bytes, filename="warzone.jpg")
        await interaction.edit_original_message(file=file, view=view, attachments=None)
        # -----------------------------------------

    @staticmethod
    async def create_operator_select(interaction, prev, current, next, view):
        # -----------------------------------------
        # Open files
        background = Image.open("resources/select/select.jpg")
        add_frame = Image.open("resources/select/addframe.png")
        middle_close = Image.open("resources/select/middle_close.png")
        # -----------------------------------------

        # -----------------------------------------
        # Display previous values
        if prev[0] is not None:
            background.paste(Image.open(f"resources/select/{prev[0]}.png").resize((452, 299)), (-87, 259))
            if prev[1] is False:
                background.paste(add_frame, (0, 259), add_frame.split()[3])
        # -----------------------------------------

        # -----------------------------------------
        # Display next values
        if next[0] is not None:
            background.paste(Image.open(f"resources/select/{next[0]}.png").resize((452, 299)), (831, 259))
            if next[1] is False:
                background.paste(add_frame, (904, 259), add_frame.split()[3])
        # -----------------------------------------

        # -----------------------------------------
        # Display current values
        if current[0] is not None:
            background.paste(Image.open(f"resources/select/{current[0]}.png"), (303, 218), Image.open(f"resources/select/{current[0]}.png").split()[3])
            if current[1] is False:
                background.paste(middle_close, (303, 218), middle_close.split()[3])
        # -----------------------------------------

        # -----------------------------------------
        # Message creation and sending
        image_bytes = io.BytesIO()
        background.save(image_bytes, format="JPEG")
        image_bytes.seek(0)
        file = disnake.File(fp=image_bytes, filename="warzone.jpg")
        await interaction.edit_original_message(file=file, view=view, attachments=None)
        # -----------------------------------------

    @staticmethod
    async def create_card_select(interaction, current, view):
        # -----------------------------------------
        # Open files
        background = Image.open("resources/card/bg.jpg")
        current_name = Image.open(f"resources/card/{current[0]}.png")
        close = Image.open("resources/card/close.png")
        # -----------------------------------------

        # -----------------------------------------
        # Display current values
        if current[1] is False:
            background.paste(current_name, (0, 0), current_name.split()[3])
            background.paste(close, (0, 0), close.split()[3])
        else:
            background.paste(current_name, (0, 0), current_name.split()[3])
        # -----------------------------------------

        # -----------------------------------------
        # Message creation and sending
        image_bytes = io.BytesIO()
        background.save(image_bytes, format="JPEG")
        image_bytes.seek(0)
        file = disnake.File(fp=image_bytes, filename="warzone.jpg")
        await interaction.edit_original_message(file=file, view=view, attachments=None)
        # -----------------------------------------
