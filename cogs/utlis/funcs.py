from __future__ import annotations
import discord
from .jsonhandeler import JsonHandeler
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont,ImageColor

## this file is made to be mess ##


def url_to_img(url):
    res = requests.get(url)
    img = Image.open(BytesIO(res.content))
    return img

def image_to_bytesio(img):
    buffer = BytesIO()
    img.save(buffer, 'png')
    buffer.seek(0)
    return buffer
