import aiohttp
from PIL import Image, ImageDraw
from io import BytesIO


class PIL:

    @staticmethod
    async def load_async_image(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    return Image.open(BytesIO(data))
                else:
                    print(f"Failed to fetch image: {response.status}")

    @staticmethod
    async def rounded_corners(img, corner_radius):
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, img.width, img.height), corner_radius, fill=255)
        rounded_img = Image.new("RGBA", img.size)
        rounded_img.paste(img, (0, 0), mask)
        return rounded_img

    @staticmethod
    async def draw_text_with_outline(draw, position, text, font, text_color, outline_color, outline_width):
        x, y = position
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
        draw.text((x, y), text, font=font, fill=text_color)
