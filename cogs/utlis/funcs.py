from __future__ import annotations
import random
import discord
import requests
from .jsonhandeler import JsonHandeler
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont,ImageColor

## this file is made to be mess ##

async def leveling(msg:discord.message.Message,level_db:JsonHandeler):
    id = msg.author.id
    exp = 4
    name = str(msg.author)
    n = level_db.fetch_data()
    if not str(id) in n["user-data"]:
        level = 0
        n["user-data"][str(id)]={'name': name,'exp': exp,'level': level}
    else:
        level = int(n["user-data"][str(id)]["exp"] ** (1/4))
        _level = n["user-data"][str(id)]["level"]
        if level > _level:
            await msg.reply(f"Hey! you just leveled up to {level}")
        __exp = n["user-data"][str(id)]["exp"]
        n["user-data"][str(id)]={'name': name,'exp': __exp + exp,'level': level}
    level_db.save(n)

def url_to_img(url):
    res = requests.get(url)
    img = Image.open(BytesIO(res.content))
    return img

def image_to_bytesio(img):
    buffer = BytesIO()
    img.save(buffer, 'png')
    buffer.seek(0)
    return buffer

class Rank:
    def __init__(self,font:str) -> None:
        self.font = ImageFont.truetype(font, 28)
        self.medium_font = ImageFont.truetype('arialbd.ttf', 22)
        self.small_font = ImageFont.truetype('arialbd.ttf', 16)

    def draw(self, ctx, rank: str, xp: str, needed_xp:str,profile_bytes) -> BytesIO:
        profile_bytes = Image.open(profile_bytes)
        user = ctx.author.name
        im = Image.new('RGBA', (400, 148), (44, 44, 44, 255))

        im_draw = ImageDraw.Draw(im)
        im_draw.text((154, 5), user, font=self.font, fill=(255, 255, 255, 255))

        rank_text = f'Level {rank}'
        im_draw.text((154, 37), rank_text, font=self.medium_font, fill=(255, 255, 255, 255))

        xp_text = f'{xp}/{needed_xp}'
        im_draw.text((154, 62), xp_text, font=self.small_font, fill=(255, 255, 255, 255))

        im_draw.rectangle((174, 95, 374, 125), fill=(64, 64, 64, 255))
        im_draw.rounded_rectangle((174, 95, 174+(int(int(xp)/int(needed_xp)*100))*2, 125),radius=1, fill=ctx.author.color.to_rgb())

        #im_draw.rectangle((0, 0, 148, 148), fill=(255, 255, 255, 255))#old pfp box data
        #im_draw.rectangle((0, 0, 148, 148), fill=(44, 44, 44, 255))
        profile_bytes = profile_bytes.resize((138,138))
        print(im.size)
        im.paste(profile_bytes, (5, 5))

        buffer = BytesIO()
        im.save(buffer, 'png')
        buffer.seek(0)

        return buffer

def filter_ban_msg(message_content):
    msg:str = message_content.lower()
    if any(word in msg for word in JsonHandeler("database/mod.json").fetch_data()["user-data"]["black-list"]["words"]):
        return True
    else:
        return False

async def etb(emb:discord.Embed):
    emb_str = "```md\n"
    emb_list = []
    try:
        emb_str += f"<{emb.author.name}>\n\n"
    except:
        pass
    try:
        emb_str += f"<{emb.title}>\n"
    except:
        pass
    try:
        if len(f"{emb_str}{emb.description}\n```")>2000:
            emb_str += "```"
            emb_list.append(emb_str)
            emb_str = "```md\n"
        emb_str += f"{emb.description}\n"
    except:
        pass
    try:
        for field in emb.fields:
            if len(f"{emb_str}#{field.name}\n{field.value}\n```")>2000:
                emb_str += "```"
                emb_list.append(emb_str)
                emb_str = "```md\n"
            emb_str += f"#{field.name}\n{field.value}\n"
    except:
        pass
    try:
        if len(f"{emb_str}\n{emb.footer.text}\n```")>2000:
            emb_str += "```"
            emb_list.append(emb_str)
            emb_str = "```md\n"
        emb_str += f"\n{emb.footer.text}\n"
    except:
        pass
    try:
        if len("{}\n{}\n```".format(emb_str, str(emb.timestamp)))>2000:
            emb_str += "```"
            emb_list.append(emb_str)
            emb_str = "```md\n"
        emb_str += "\n{}".format(str(emb.timestamp))
    except:
        pass
    emb_str += "```"
    if emb_str != "```md\n```":
        emb_list.append(emb_str)
    return emb_list

def gen(lenght:int=5):
    database = JsonHandeler("cogs/utlis/global_var.json")
    data = database.fetch_data()
    x = True
    while x:
        t= _gen(lenght)
        if t in data["system"]["used_gen_token"]:
            continue
        else:
            data["system"]["used_gen_token"].append(t)
            database.save(data)
            break
    return t
def _gen(lenght):
    list_ = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    list_s = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    list_num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", '9']
    x =""
    for i in range(lenght):
        type_ = random.choice([1,2,3])
        if type_ == 1:
            x+=random.choice(list_)
        if type_ == 2:
            x+=random.choice(list_s)
        if type_ == 3:
            x+=random.choice(list_num)
    return x

