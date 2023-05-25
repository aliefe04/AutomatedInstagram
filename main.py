from PIL import Image, ImageDraw, ImageFont
import textwrap
import json
from instabot import Bot
import os
import random


def image_generator(text, author, savename, background_color, font_color):
    image = Image.new("RGB", (1080, 1350), background_color)

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("src/fonts/font.otf", size=50)
    margin = 40
    offset = 540
    line_spacing = 30
    lines = textwrap.wrap(text, width=40)
    total_height = sum(font.getsize(line)[1] for line in lines) + line_spacing * (
        len(lines) - 1
    )

    y_offset = (image.height - total_height - margin * 2) // 2

    for line in lines:
        line_width, line_height = font.getsize(line)
        x_offset = (image.width - line_width) // 2
        draw.text((x_offset, y_offset), line, font=font, fill=font_color)
        y_offset += line_height + line_spacing

    if author is not None and author.strip() != '':
        attribution_font = ImageFont.truetype("src/fonts/font.otf", size=30)
        attribution_width, attribution_height = attribution_font.getsize(author)
        attribution_offset = (
            (image.width - attribution_width) // 2,
            y_offset + margin,
        )
        draw.text(attribution_offset, author, font=attribution_font, fill=font_color)

    watermark_font = ImageFont.truetype("src/fonts/watermark.ttf", size=70)
    watermark_text = "More Potentials"
    watermark_width, watermark_height = watermark_font.getsize(watermark_text)
    watermark_offset = (
        (image.width - watermark_width) // 2,
        image.height - watermark_height - margin,
    )
    draw.text(watermark_offset, watermark_text, font=watermark_font, fill=font_color)

    image.save(savename)


def run_image_generator():
    json_path = "src/json/quotes.json"
    with open(json_path) as f:
        data = json.load(f)

    used_path = "src/json/used.json"
    used_quotes = []
    try:
        with open(used_path) as f:
            used_quotes = json.load(f)
    except FileNotFoundError:
        pass

    num_quotes = 3
    random_quotes = random.sample(data["quotes"], num_quotes)
    for i, quote in enumerate(random_quotes):
        if i == 0:  # 1
            background_color = "#4D455D" # EN SAĞ
            font_color = "white"
        elif i == len(random_quotes) - 1:  # 3
            background_color = "#7DB9B6" # EN SOL
            font_color = "white"
        else:  # 2
            background_color = "#E96479" # ORTA
            font_color = "white"
        savename = f"src/generated/quote{i+1}.jpg"
        image_generator(
            quote["quote"],
            quote["author"],
            savename,
            background_color,
            font_color=font_color,
        )
        used_quotes.append(quote)
        data["quotes"].remove(quote)

    with open(json_path, "w") as f:
        json.dump(data, f)

    with open(used_path, "w") as f:
        json.dump(used_quotes, f)


def post_to_instagram():
    # Load Instagram account credentials from config file
    with open('src/json/config.json', 'r') as f:
        config = json.load(f)
    username = config['username']
    password = config['password']

    # Log in to Instagram account
    bot = Bot()
    bot.login(username=username, password=password)

    # Upload photos from generated directory
    filenames = os.listdir('src/generated')[:3]
    for filename in filenames:
        bot.upload_photo(f'src/generated/{filename}')

    # Delete uploaded photos
    for filename in filenames:
        os.remove(f'src/generated/{filename}.REMOVE_ME')


run_image_generator()
post_to_instagram()