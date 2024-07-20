import io
import asyncio
import disnake
from PIL import Image, ImageDraw, ImageFont
from utils.pillow import PIL


class CasesBuilder:
    _pil = PIL

    @staticmethod
    async def create_open_case_view(interaction, cases):
        # -----------------------------------------
        # Open files
        background = Image.open("resources/cases/open.png")
        draw = ImageDraw.Draw(background)
        agencyfb_bold = "resources/fonts/agencyfb_bold.ttf"
        # -----------------------------------------

        # -----------------------------------------
        # Text
        draw.text((111, 604), f"{cases["sixth_case"]}", fill="#e1e1e1", font=ImageFont.truetype(agencyfb_bold, size=26))
        draw.text((425, 604), f"{cases["fifth_case"]}", fill="#e1e1e1", font=ImageFont.truetype(agencyfb_bold, size=26))
        draw.text((732, 604), f"{cases["fourth_case"]}", fill="#e1e1e1", font=ImageFont.truetype(agencyfb_bold, size=26))
        draw.text((1005, 604), f"{cases["total_case"]}", fill="#e1e1e1", font=ImageFont.truetype(agencyfb_bold, size=26))
        draw.text((111, 671), f"{cases["first_case"]}", fill="#e1e1e1", font=ImageFont.truetype(agencyfb_bold, size=26))
        draw.text((425, 671), f"{cases["second_case"]}", fill="#e1e1e1", font=ImageFont.truetype(agencyfb_bold, size=26))
        draw.text((732, 671), f"{cases["third_case"]}", fill="#e1e1e1", font=ImageFont.truetype(agencyfb_bold, size=26))
        # -----------------------------------------

        # -----------------------------------------
        # Message creation and sending
        image_bytes = io.BytesIO()
        background.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        file = disnake.File(fp=image_bytes, filename="warzone.png")
        await interaction.edit_original_message(file=file, attachments=None)
        # -----------------------------------------

    @staticmethod
    async def create_case(interaction, coin, view, name):
        await interaction.response.defer()
        # -----------------------------------------
        # Open files
        background = Image.open(f"resources/cases/{name}.png")
        draw = ImageDraw.Draw(background)
        agencyfb_bold = "resources/fonts/agencyfb_bold.ttf"
        # -----------------------------------------

        # -----------------------------------------
        # Text
        draw.text((1108, 36), f"{coin} CP", fill="#dfdfdf", font=ImageFont.truetype(agencyfb_bold, size=40))
        # -----------------------------------------

        # -----------------------------------------
        # Message creation and sending
        image_bytes = io.BytesIO()
        background.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        file = disnake.File(fp=image_bytes, filename="warzone.png")
        await interaction.edit_original_message(file=file, view=view, attachments=None)
        # -----------------------------------------

    @staticmethod
    async def create_awards_case(interaction, items, coin, view):
        # -----------------------------------------
        # Open files
        color = "white"
        coo_y = 369
        if items[2] == "common":
            file_gif = disnake.File('resources/cases/common.gif', filename='common.gif')
            await interaction.edit_original_message(file=file_gif, attachments=None)
            color = "#71748c"
        elif items[2] == "uncommon":
            file_gif = disnake.File('resources/cases/uncommon.gif', filename='uncommon.gif')
            await interaction.edit_original_message(file=file_gif, attachments=None)
            color = "#1d6046"
        elif items[2] == "mythical":
            file_gif = disnake.File('resources/cases/mythical.gif', filename='mythical.gif')
            await interaction.edit_original_message(file=file_gif, attachments=None)
            color = "#513280"
            coo_y = 382
        elif items[2] == "ancient":
            file_gif = disnake.File('resources/cases/ancient.gif', filename='ancient.gif')
            await interaction.edit_original_message(file=file_gif, attachments=None)
            color = "#7f2720"
            coo_y = 382
        elif items[2] == "immortal":
            file_gif = disnake.File('resources/cases/immortal.gif', filename='immortal.gif')
            await interaction.edit_original_message(file=file_gif, attachments=None)
            color = "#dabe66"
            coo_y = 369
        await asyncio.sleep(6.5)
        background = Image.open("resources/cases/award.jpg")
        draw = ImageDraw.Draw(background)
        agencyfb_bold = "resources/fonts/agencyfb_bold.ttf"
        # -----------------------------------------

        # -----------------------------------------
        # Text
        background.paste(Image.open(f"resources/cases/{items[4]}/{items[0]}.png"), (10, 165), Image.open(f"resources/cases/{items[4]}/{items[0]}.png").split()[3])
        draw.text((667, 262), f"{items[1]}", color='white', font=ImageFont.truetype(agencyfb_bold, size=42))
        draw.text((651, 315), f"{items[3]}", color='white', font=ImageFont.truetype(agencyfb_bold, size=42))
        draw.text((678, coo_y), f"{items[2]}", color=color, font=ImageFont.truetype(agencyfb_bold, size=42))
        draw.text((711, 661), f"{coin} CP", color='#dfdfdf', font=ImageFont.truetype(agencyfb_bold, size=42))
        # -----------------------------------------

        # -----------------------------------------
        # Message creation and sending
        image_bytes = io.BytesIO()
        background.save(image_bytes, format="JPEG")
        image_bytes.seek(0)
        file = disnake.File(fp=image_bytes, filename="warzone.jpg")
        await interaction.edit_original_message(file=file, view=view, attachments=None)
        # -----------------------------------------
