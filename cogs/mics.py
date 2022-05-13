import discord,time,io
from discord.ext import commands,tasks
from cogs.utlis.jsonhandeler import JsonHandeler
import discord.ext.commands as disext
from PIL import Image,ImageColor,ImageDraw,ImageFont
import os
from cogs.utlis.funcs import image_to_bytesio

def list_list_px_to_img(List,bg="WHITE"):
    img2=Image.new('RGB', (500*2, 500*2), bg)
    im = ImageDraw.Draw(img2)
    posy = 0
    for i in List:
            posx = 0
            for n in i:
                im.rectangle((posx*20+1,posy*20+1,posx*20+1+18,posy*20+1+18),(n[0],n[1],n[2]))
                posx += 1
            posy += 1
    return img2

class Mics(commands.Cog, name="misc"):
    def __init__(self, bot):
        self.bot = bot
        self.update_canves.start()
    
    @tasks.loop(seconds=60)
    async def update_canves(self):
        one_one = JsonHandeler("place_lists/1_1.json").fetch_data()
        one_two = JsonHandeler("place_lists/1_2.json").fetch_data()
        one_three = JsonHandeler("place_lists/1_3.json").fetch_data()
        two_one = JsonHandeler("place_lists/2_1.json").fetch_data()
        two_two = JsonHandeler("place_lists/2_2.json").fetch_data()
        two_three = JsonHandeler("place_lists/2_3.json").fetch_data()
        list_list_px_to_img(one_one).save("images/place/1_1.png","PNG")
        list_list_px_to_img(one_two).save("images/place/1_2.png","PNG")
        list_list_px_to_img(one_three).save("images/place/1_3.png","PNG")
        list_list_px_to_img(two_one).save("images/place/2_1.png","PNG")
        list_list_px_to_img(two_three).save("images/place/2_3.png","PNG")
        list_list_px_to_img(two_two).save("images/place/2_2.png","PNG")
        
    @commands.command()
    async def canvas(self,ctx):
        img=Image.new('RGB', (1080, 720), "WHITE")
        img.paste(Image.open("images/place/1_1.png").resize((360,360)),(0,0))
        img.paste(Image.open("images/place/1_2.png").resize((360,360)),(361,0))
        img.paste(Image.open("images/place/1_3.png").resize((360,360)),(722,0))
        img.paste(Image.open("images/place/2_1.png").resize((360,360)),(0,361))
        img.paste(Image.open("images/place/2_2.png").resize((360,360)),(361,361))
        img.paste(Image.open("images/place/2_3.png").resize((360,360)),(722,361))
        img_by = image_to_bytesio(img)
        await ctx.send(content="beta test",file=discord.File(img_by,filename="canvas.png"))

    @commands.command()
    async def subcanvas(self,ctx,canvas_id:int=None):
        if canvas_id is None or canvas_id>6:
            img_by = image_to_bytesio(Image.open("images/sub/subcanvas.png"))
            await ctx.send(content="canvas is divided into __6__ parts so u can see the pixel coords \n \n The below image shows the id of corresponding parts of the canvas \n use <subcanvas {id}> ",file=discord.File(img_by,filename="subcanvas.png"))
            return
        if canvas_id == 1:
            img=Image.open("images/sub/1_1.png")
            _l = JsonHandeler("place_lists/1_1.json").fetch_data()
            img.paste(list_list_px_to_img(_l,bg="BLACK"),(20,20))
            img_by = image_to_bytesio(img)
            await ctx.send(file=discord.File(img_by,filename="1_1.png"))
        if canvas_id == 2:
            img=Image.open("images/sub/1_2.png")
            _l = JsonHandeler("place_lists/1_2.json").fetch_data()
            img.paste(list_list_px_to_img(_l,bg="BLACK"),(20,20))
            img_by = image_to_bytesio(img)
            await ctx.send(file=discord.File(img_by,filename="1_1.png"))
        if canvas_id == 1:
            img=Image.open("images/sub/1_1.png")
            _l = JsonHandeler("place_lists/1_1.json").fetch_data()
            img.paste(list_list_px_to_img(_l,bg="BLACK"),(20,20))
            img_by = image_to_bytesio(img)
            await ctx.send(file=discord.File(img_by,filename="1_2.png"))
        if canvas_id == 3:
            img=Image.open("images/sub/1_3.png")
            _l = JsonHandeler("place_lists/1_3.json").fetch_data()
            img.paste(list_list_px_to_img(_l,bg="BLACK"),(20,20))
            img_by = image_to_bytesio(img)
            await ctx.send(file=discord.File(img_by,filename="1_3.png"))
        if canvas_id == 4:
            img=Image.open("images/sub/2_1.png")
            _l = JsonHandeler("place_lists/2_1.json").fetch_data()
            img.paste(list_list_px_to_img(_l,bg="BLACK"),(20,20))
            img_by = image_to_bytesio(img)
            await ctx.send(file=discord.File(img_by,filename="2_1.png"))
        if canvas_id == 5:
            img=Image.open("images/sub/2_2.png")
            _l = JsonHandeler("place_lists/2_2.json").fetch_data()
            img.paste(list_list_px_to_img(_l,bg="BLACK"),(20,20))
            img_by = image_to_bytesio(img)
            await ctx.send(file=discord.File(img_by,filename="2_2.png"))
        if canvas_id == 6:
            img=Image.open("images/sub/2_3.png")
            _l = JsonHandeler("place_lists/2_3.json").fetch_data()
            img.paste(list_list_px_to_img(_l,bg="BLACK"),(20,20))
            img_by = image_to_bytesio(img)
            await ctx.send(file=discord.File(img_by,filename="2_3.png"))
        else:
            return

    @commands.command()
    async def place(self,ctx,posx:str,posy:str,color):
        if len(posy) !=2 or len(posx) !=2:
            await ctx.send("invalid \n correct formate is /n `.place <[a to l,t,n to o][0 to 9]> <[a to j][0 to 9]> <hex_color_code>`\n eg .place a0 b1 #ff0000")
            return
        posx = posx.lower()
        posy = posy.lower()
        x = posx.lower()
        y = posy.lower()
        a = {
            "a": "0+",
            "b": "10+",
            "c": "20+",
            "d": "30+",
            "e": "40+",
            "f": "50+",
            "g": "60+",
            "h": "70+",
            "i": "80+",
            "j": "90+",
            "k": "100+",
            "l": "110+",
            "t": "120+",
            "n": "130+",
            "o": "140+"
        }
        for i in a:
            posx = posx.replace(str(i),str(a[i]))
            posy = posy.replace(str(i),str(a[i]))
        try:
            posx = int(eval(posx))
            posy = int(eval(posy))
        except Exception as e :
            await ctx.send("Invalid coords"+e)
            return
        if posx >149 or posy > 99:
            await ctx.send("coords out of range")
            return
        if list(x)[0] in ["a","b","c","d","e"]:
            u = "1"
        elif list(x)[0] in ["f","g","h","i","j"]:
            u = "2"
        elif list(x)[0] in ["k","l","t","n","0"]:
            u = "3"
        else:
            return
        if list(y)[0] in ["a","b","c","d","e"]:
            v = "1"
        elif list(y)[0] in ["f","g","h","i","j"]:
            v = "2"
        else:
            return
        database = JsonHandeler(f"place_lists/{u}_{v}.json")
        data = database.fetch_data()
        data[posy][posx] = ImageColor.getrgb(color)
        database.save(data)
        img=Image.open(f"images/sub/{u}_{v}.png")
        img.paste(list_list_px_to_img(data,bg="BLACK"),(20,20))
        img_by = image_to_bytesio(img)
        await ctx.send(file=discord.File(img_by,filename=f"{u}_{v}.png"))
