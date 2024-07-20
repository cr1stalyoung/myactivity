import io
import disnake
from PIL import Image, ImageDraw, ImageFont
from utils.division import Division
from utils.prestige import Level
from utils.pillow import PIL


class RankingBuilder:
    _division = Division
    _pil = PIL
    _level = Level

    @classmethod
    async def create_image_server(cls, interaction, user_data, top_data, bot, view):
        # -----------------------------------------
        # Variables
        link_avatar = "https://img.icons8.com/external-justicon-flat-justicon/1x/external-discord-social-media-justicon-flat-justicon.png"
        guild_avatar_url = interaction.guild.icon.url if interaction.guild.icon else link_avatar
        interaction_avatar_url = interaction.user.avatar.url if interaction.user.avatar else link_avatar
        interaction_name = interaction.author.display_name
        # Fonts
        calibri_bold = "resources/fonts/calibri_bold.ttf"
        # Co-ordinates
        avatar_y = 113
        text_y = 123
        icon_y = 104
        frame_y = 115
        prestige_y = 120
        # Image loading and drawing
        background = Image.open("resources/ranking/server.jpg")
        draw = ImageDraw.Draw(background)
        # -----------------------------------------

        # -----------------------------------------
        # Unpacking user data
        for item in top_data:
            user_id, level, count_msg, count_voice, voice_month, score, ranking = item['user_id'], item['level'], item['count_msg'], item['count_voice'], item['voice_month'], item['score'], item['ranking']
            # Ranked icon
            if score >= 10000 and ranking <= 50:
                top50 = Image.open("resources/ranking/top50.png").resize((50, 59))
                background.paste(top50, (204, icon_y), top50.split()[3])
            else:
                icon_rank = await cls._division.definition_server(score)
                icon_rank = Image.open(icon_rank).resize((50, 59))
                background.paste(icon_rank, (204, icon_y), icon_rank.split()[3])
            # Member name and avatar
            try:
                member = await bot.fetch_user(user_id)
                member_name = (member.display_name[:14] + '...') if len(member.display_name) > 14 else member.display_name
                member_avatar_url = member.avatar.url if member.avatar else link_avatar
            except disnake.errors.NotFound:
                member_name = "Unknown user"
                member_avatar_url = link_avatar
            # Data output
            member_avatar = await cls._pil.load_async_image(member_avatar_url)
            background.paste(member_avatar.resize((40, 40)), (379, avatar_y))
            draw.text((110, text_y), f"#{ranking}", color='#a5a5a4', font=ImageFont.truetype(calibri_bold, size=25))
            draw.text((258, text_y), f"{score}", color='#a5a5a4', font=ImageFont.truetype(calibri_bold, size=25))
            draw.text((429, text_y), member_name, color='#a5a5a4', font=ImageFont.truetype(calibri_bold, size=25))
            draw.text((697, text_y), f"{max(0, int(voice_month / 60))} h.", color='#a5a5a4', font=ImageFont.truetype(calibri_bold, size=25))
            frame = Image.open("resources/ranking/frame.png").resize((40, 40))
            prestige_image = await cls._level.get_image(level)
            prestige = Image.open(f"resources/level/{prestige_image[0]}").resize((30, 30))
            background.paste(frame, (1001, frame_y), frame.split()[3])
            background.paste(prestige, (1006, prestige_y), prestige.split()[3])
            draw.text((1049, text_y), f"{level}", color='#a5a5a4', font=ImageFont.truetype(calibri_bold, size=25))
            draw.text((1186, text_y), f"{max(0, int(count_voice / 60))} h.", color='#a5a5a4', font=ImageFont.truetype(calibri_bold, size=25))
            draw.text((1356, text_y), f"{count_msg} m.", color='#a5a5a4', font=ImageFont.truetype(calibri_bold, size=25))
            avatar_y, text_y, icon_y, frame_y, prestige_y = map(lambda x: x + 57, (avatar_y, text_y, icon_y, frame_y, prestige_y))
        # -----------------------------------------

        # -----------------------------------------
        # Display avatar and name
        avatar = await cls._pil.load_async_image(interaction_avatar_url)
        avatar = await cls._pil.rounded_corners(avatar, 32)
        background.paste(avatar.resize((225, 225)), (106, 730), avatar.resize((225, 225)).split()[3])
        frame = Image.open("resources/icon/frame.png").resize((225, 225))
        background.paste(frame, (106, 730), frame.split()[3])
        draw.text((350, 732), f"{interaction_name}", color="white", font=ImageFont.truetype(calibri_bold, size=45))
        # Display guild data
        guild_avatar_url = await cls._pil.load_async_image(guild_avatar_url)
        background.paste(guild_avatar_url.resize((38, 38)), (356, 773))
        draw.text((406, 779), f"{interaction.guild.name.upper()}", color='#a5a5a4', font=ImageFont.truetype(calibri_bold, size=30))
        # -----------------------------------------

        # -----------------------------------------
        # Unpacking interaction data
        level, count_msg, count_voice, score, ranking, score, ranking = user_data['level'], user_data['count_msg'], user_data['count_voice'], user_data['score'], user_data['ranking'], user_data['score'], user_data['ranking']
        # Ranked icon
        if score >= 10000 and ranking <= 50:
            top50 = Image.open("resources/ranking/top50.png").resize((74, 84))
            background.paste(top50, (496, 862), top50.split()[3])
        else:
            icon_rank = await cls._division.definition_server(score)
            top50 = Image.open(icon_rank).resize((74, 84))
            background.paste(top50, (496, 862), top50.split()[3])
        # Data output
        draw.text((358, 889), f"#{ranking}", color='#a5a5a4', font=ImageFont.truetype(calibri_bold, size=32))
        draw.text((575, 887), f"{score}", color='#a5a5a4', font=ImageFont.truetype(calibri_bold, size=38))
        draw.text((777, 887), f"{level}", color='#a5a5a4', font=ImageFont.truetype(calibri_bold, size=38))
        draw.text((951, 887), f"{max(0, int(count_voice / 60))} h.", color='#a5a5a4', font=ImageFont.truetype(calibri_bold, size=38))
        draw.text((1167, 887), f"{count_msg} m.", color='#a5a5a4', font=ImageFont.truetype(calibri_bold, size=38))
        # -----------------------------------------

        # -----------------------------------------
        # Message creation and sending
        image_bytes = io.BytesIO()
        background.save(image_bytes, format="JPEG")
        image_bytes.seek(0)
        file = disnake.File(fp=image_bytes, filename="warzone.jpg")
        await interaction.edit_original_message(file=file, view=view, attachments=None)
        # -----------------------------------------

    @classmethod
    async def create_image_global(cls, interaction, user_data, top_data, view):
        # -----------------------------------------
        # Variables
        top50 = Image.open("resources/ranking/top50.png").resize((58, 72))
        # Fonts
        calibri_bold = "resources/fonts/calibri_bold.ttf"
        # Co-ordinates
        old_rank_y = 61
        rank_y = 62
        score_y = 61
        top50_y = 40
        division_y = 36
        avatar_y = 56
        name_y = 62
        card_y = 42
        div_change = 62
        text_change = 65
        # Image loading and drawing
        background = Image.open("resources/ranking/global.jpg")
        draw = ImageDraw.Draw(background)
        # -----------------------------------------

        # -----------------------------------------
        # Unpacking top data
        for item in top_data:
            score, card, _, old_score, old_rank, ranking, url, display_name = item['score'], item['card'], item['user_id'], item['old_score'], item['old_rank'], item['ranking'], item['url'], item['name']
            # Card member
            if card is not None:
                card = Image.open(f"resources/ranking/cards/{card}.png")
                background.paste(card, (583, card_y), card.split()[3])
            # Position difference
            pos_diff = old_rank - ranking
            if pos_diff > 0:
                pos_diff_image = Image.open("resources/ranking/up.png")
                background.paste(pos_diff_image, (598, old_rank_y), pos_diff_image.split()[3])
            elif pos_diff < 0:
                pos_diff_image = Image.open("resources/ranking/down.png")
                background.paste(pos_diff_image, (598, old_rank_y), pos_diff_image.split()[3])
            # Ranked icon
            if score >= 10000 and ranking <= 50:
                background.paste(top50, (673, top50_y), top50.split()[3])
            else:
                icon_rank = await cls._division.definition_server(score)
                icon_rank = Image.open(icon_rank).resize((65, 85))
                background.paste(icon_rank, (670, division_y), icon_rank.split()[3])
            # Data output
            member_avatar = await cls._pil.load_async_image(url)
            background.paste(member_avatar.resize((40, 40)), (736, avatar_y))
            draw.text((631, rank_y), f"{ranking}", color='#cdcdcd', font=ImageFont.truetype(calibri_bold, size=32))
            draw.text((786, name_y), f"{display_name}", color='#cdcdcd', font=ImageFont.truetype(calibri_bold, size=33))
            draw.text((1333, score_y), f"{score}", color='#cdcdcd', font=ImageFont.truetype(calibri_bold, size=34))
            # Get change ranking
            score_difference = score - old_score
            score_difference = max(-9999, min(score_difference, 9999))
            score_difference_image = await cls._division.change_world_rank(score_difference)
            score_difference_image = Image.open(score_difference_image)
            background.paste(score_difference_image, (1454, div_change), score_difference_image.split()[3])
            if score_difference < 0:
                draw.text((1462, text_change), f"{score_difference}", color='red', font=ImageFont.truetype(calibri_bold, size=25))
            else:
                draw.text((1462, text_change), f"+{score_difference}", color='red', font=ImageFont.truetype(calibri_bold, size=25))
            card_y, old_rank_y, avatar_y, name_y, score_y, rank_y, top50_y, division_y, div_change, text_change = map(lambda x: x + 83, (card_y, old_rank_y, avatar_y, name_y, score_y, rank_y, top50_y, division_y, div_change, text_change))
        # -----------------------------------------

        # -----------------------------------------
        # Unpacking user data
        for item in user_data:
            score_user, card_user, old_score_user, old_rank_user, ranking_user = item['score'], item['card'], item['old_score'], item['old_rank'], item['ranking']
            # Card member
            if card_user is not None:
                card_user = Image.open(f"resources/ranking/cards/{card_user}.png")
                background.paste(card_user, (583, 903), card_user.split()[3])
            # Position difference
            pos_diff_user = old_rank_user - ranking_user
            if pos_diff_user > 0:
                pos_diff_image = Image.open("resources/ranking/up.png")
                background.paste(pos_diff_image, (598, 925), pos_diff_image.split()[3])
            elif pos_diff_user < 0:
                pos_diff_image = Image.open("resources/ranking/down.png")
                background.paste(pos_diff_image, (598, 925), pos_diff_image.split()[3])
            else:
                pass
            # Ranked icon
            if score_user >= 10000 and ranking_user <= 50:
                background.paste(top50, (720, 902), top50.split()[3])
            else:
                icon_rank_user = await cls._division.definition_server(score_user)
                icon_rank_user = Image.open(icon_rank_user).resize((65, 85))
                background.paste(icon_rank_user, (720, 897), icon_rank_user.split()[3])
            # Data output
            user_avatar = await cls._pil.load_async_image(interaction.user.avatar.url)
            background.paste(user_avatar.resize((40, 40)), (787, 917))
            draw.text((631, 926), f"{ranking_user}", color='#cdcdcd', font=ImageFont.truetype(calibri_bold, size=32))
            draw.text((837, 924), "YOU", color='#cdcdcd', font=ImageFont.truetype(calibri_bold, size=32))
            draw.text((1333, 923), f"{score_user}", color='#cdcdcd', font=ImageFont.truetype(calibri_bold, size=34))
            # Get change ranking
            score_difference_user = score_user - old_score_user
            score_difference_user = max(-9999, min(score_difference_user, 9999))
            score_difference_image_user = await cls._division.change_world_rank(score_difference_user)
            score_difference_image_user = Image.open(score_difference_image_user)
            background.paste(score_difference_image_user, (1454, 923), score_difference_image_user.split()[3])
            if score_difference_user < 0:
                draw.text((1462, 926), f"{score_difference_user}", color='red', font=ImageFont.truetype(calibri_bold, size=25))
            else:
                draw.text((1462, 926), f"+{score_difference_user}", color='red', font=ImageFont.truetype(calibri_bold, size=25))
        # -----------------------------------------

        # -----------------------------------------
        # Message creation and sending
        image_bytes = io.BytesIO()
        background.save(image_bytes, format="JPEG")
        image_bytes.seek(0)
        file = disnake.File(fp=image_bytes, filename="warzone.jpg")
        await interaction.edit_original_message(file=file, view=view, attachments=None)
        # -----------------------------------------
