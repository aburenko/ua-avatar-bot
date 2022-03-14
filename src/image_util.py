from PIL import Image
from PIL import ImageDraw
import numpy as np
from typing import Tuple, Final

border: Final[Tuple] = (50, 50)


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def create_circle_image(overlay_path):
    # Open the input image as numpy array, convert to RGB
    img = crop_max_square(Image.open(overlay_path).convert("RGB"))
    np_image = np.array(img)
    h, w = img.size

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)

    # Convert alpha Image to numpy array
    np_alpha = np.array(alpha)

    # Add alpha layer to RGB
    np_image = np.dstack((np_image, np_alpha))

    res = Image.fromarray(np_image)
    # Save with alpha
    return res


def add_background(background_path, overlay_path, output_path):
    background = Image.open(background_path).convert("RGBA")
    overlay = create_circle_image(overlay_path).resize(np.subtract(background.size, border))
    overlay.save(overlay_path, "PNG")

    margin_to_overlay = tuple(int(i / 2) for i in border)
    background.paste(overlay, margin_to_overlay, overlay)
    background.save(output_path, "PNG")
