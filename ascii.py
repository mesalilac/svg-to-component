import sys
from typing import Tuple, cast
from pathlib import Path
from PIL import Image
import io
import cairosvg


def image_to_ascii(image: Image.Image, width: int = 40) -> str:
    aspect_ratio = image.height / image.width
    height = int(width * aspect_ratio * 0.55)
    image = image.resize((width, height))

    ascii_lines = []

    for y in range(image.height):
        row = []
        for x in range(image.width):
            pixel = cast(Tuple[int, int, int, int], image.getpixel((x, y)))
            _, _, _, a = pixel

            if a < 40:
                row.append(" ")
            elif a < 100:
                row.append("░")
            elif a < 180:
                row.append("▒")
            elif a < 230:
                row.append("▓")
            else:
                row.append("█")

        ascii_lines.append("".join(row))

    return "\n".join(ascii_lines)


def svg_to_ascii(svg_path: Path, width: int = 40) -> str:
    png_data = cairosvg.svg2png(url=str(svg_path), background_color=None)
    image = Image.open(io.BytesIO(png_data)).convert("RGBA")

    return image_to_ascii(image, width)
