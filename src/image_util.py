from PIL import Image
from PIL import ImageDraw
import numpy as np


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
    npImage = np.array(img)
    h, w = img.size

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)

    # Convert alpha Image to numpy array
    npAlpha = np.array(alpha)

    # Add alpha layer to RGB
    npImage = np.dstack((npImage, npAlpha))

    res = Image.fromarray(npImage)
    # Save with alpha
    return res


def add_background(background_path, overlay_path, output_path):
    background = Image.open(background_path).convert("RGBA")
    overlay = create_circle_image(overlay_path).resize(np.subtract(background.size, (50, 50)))
    overlay.save(overlay_path, "PNG")

    background.paste(overlay, (25, 25), overlay)
    background.save(output_path, "PNG")
