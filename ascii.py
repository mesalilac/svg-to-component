import sys
from typing import Tuple, cast
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from pathlib import Path
from PIL import Image
import io


def image_to_ascii(image: Image.Image, width: int = 40) -> str:
    image = image.convert("RGB")

    aspect_ratio = image.height / image.width
    height = int(width * aspect_ratio * 0.55)
    image = image.resize((width, height))

    ascii_lines = []

    for y in range(image.height):
        row = []
        for x in range(image.width):
            pixel = cast(Tuple[int, int, int], image.getpixel((x, y)))
            r, g, b = pixel

            if not (r > 245 and g > 245 and b > 245):
                row.append("█")
            else:
                row.append(" ")

        ascii_lines.append("".join(row))

    return "\n".join(ascii_lines)


def svg_to_ascii(svg_path: Path, width: int = 40) -> str:
    drawing = svg2rlg(svg_path)
    if drawing is None:
        raise ValueError("Failed to load SVG")

    png_data = renderPM.drawToString(drawing, fmt="PNG")
    image = Image.open(io.BytesIO(png_data))

    return image_to_ascii(image, width)


if __name__ == "__main__":
    print(svg_to_ascii(sys.argv[1], width=24))
