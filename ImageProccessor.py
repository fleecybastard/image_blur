from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
from math import ceil


class ImageProcessor:
    watermark_height_percent = 4
    watermark_padding_vertical = 0
    watermark_padding_start = 30
    text_height_percent = 8
    padding_vertical = 20
    padding_start = 5
    input_text = "FAKE "
    fill = (255, 27, 23)
    font_file = "fonts/Lato-Bold.ttf"

    @staticmethod
    def process_image(image_bytes: bytes,
                      blur: bool = False,
                      watermark: bool = False,
                      bot_name: str = None) -> bytes:
        if watermark and bot_name is None:
            watermark = False
        bytes_input = io.BytesIO(image_bytes)

        image = Image.open(bytes_input)
        if blur:
            # image = image.filter(ImageFilter.GaussianBlur(8))
            image = ImageProcessor._blur(image)

        d = ImageDraw.Draw(image)
        picture_height = image.height
        picture_width = image.width

        text_height = int(picture_height * ImageProcessor.text_height_percent / 100)

        font = ImageFont.truetype(font=ImageProcessor.font_file, size=text_height)

        text_len = font.getlength(ImageProcessor.input_text)

        write_text = ImageProcessor.input_text * (int(picture_width / text_len) + 1)

        bottom_text_vertical_padding = picture_height - text_height - ImageProcessor.padding_vertical

        d.text((ImageProcessor.padding_start, bottom_text_vertical_padding),
               write_text, fill=ImageProcessor.fill, font=font)
        d.text((ImageProcessor.padding_start, ImageProcessor.padding_vertical), write_text,
               fill=ImageProcessor.fill, font=font, anchor="lt")

        # BOTTOM WATERMARK
        # if watermark:
        #     watermark_height = int(picture_height * ImageProcessor.watermark_height_percent / 100)
        #     watermark_font = ImageFont.truetype(font=ImageProcessor.font_file, size=watermark_height)
        #     d.text((ImageProcessor.watermark_padding_start,
        #             bottom_text_vertical_padding - watermark_height - ImageProcessor.watermark_padding_vertical),
        #            bot_name, fill=ImageProcessor.fill, font=watermark_font, anchor="lt")
        # TOP WATERMARK
        if watermark:
            watermark_height = int(picture_height * ImageProcessor.watermark_height_percent / 100)
            watermark_font = ImageFont.truetype(font=ImageProcessor.font_file, size=watermark_height)
            d.text((ImageProcessor.watermark_padding_start,
                    ImageProcessor.padding_vertical + text_height + ImageProcessor.watermark_padding_vertical),
                   bot_name, fill=ImageProcessor.fill, font=watermark_font, anchor="lt")

        bytes_file = io.BytesIO()

        image.save(bytes_file, format="png")

        bytes_file.seek(0)
        return bytes_file.getvalue()

    @staticmethod
    def _blur(image: Image.Image) -> Image.Image:
        square_size = 60  # 120
        blur_radius = 18
        k = 0
        need_plus = ceil(image.width / square_size) % 2 == 0
        for j in range(0, image.height, square_size):
            for i in range(0, image.width, square_size):
                if k % 2 == 0:
                    k += 1
                    continue
                square = image.crop((i, j, i + square_size, j + square_size))
                square = square.filter(ImageFilter.GaussianBlur(blur_radius))
                image.paste(square, (i, j))
                k += 1
            if need_plus:
                k += 1
        return image
