import random
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def get_random_aesthetic_color():
    # Define a list of aesthetic colors in RGB format.
    aesthetic_colors = [
        (255, 102, 102),  # Red
        (255, 204, 102),  # Orange
        (255, 255, 102),  # Yellow
        (102, 255, 102),  # Green
        (102, 204, 255),  # Blue
        (204, 102, 255),  # Purple
        (255, 153, 204),  # Pink
        (102, 102, 102),  # Gray
        (153, 153, 255),  # Lavender
        (51, 204, 204),  # Teal
    ]

    # Choose a random color from the list.
    return random.choice(aesthetic_colors)


def create_image(user_name: str, ASSETS_ROOT=None):
    name = user_name
    if not name:
        print("Name cannot be empty.")
        return

    try:
        # Split the name if there are more than one word.
        split = name.split(' ')
        # Get the first letter from the first two words.
        text = '{}{}'.format(split[0][0], split[1][0])
    except:
        # If the name has only one word, get the first letter.
        text = name[0]

    # Get a random background color.
    color = get_random_aesthetic_color()

    # Create a new image with the chosen background color.
    image = Image.new('RGB', (288, 288), color=color)

    # Load the font file (Roboto-Bold.ttf) if it exists in the current directory.
    font_path = 'app/authentication/Roboto-Bold.ttf'
    print(os.path.exists(font_path))
    if os.path.exists(font_path):
        font_type = ImageFont.truetype(font=font_path, size=150)
        draw = ImageDraw.Draw(image)

        # Get the bounding box for the text to determine its size.
        bbox = draw.textbbox((0, 0), text=text.upper(), font=font_type)
        width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # Calculate the position to center the text on the image.
        x = (288 - width) / 2
        y = (288 - height) / 2

        draw.text((x, y), text=text.upper(), fill=(255, 255, 255), font=font_type)

        image_buffer = BytesIO()
        image.save(image_buffer, format="PNG")
        image_data = image_buffer.getvalue()

        return image_data
    else:
        return False
