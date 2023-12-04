#
# Copyright (C) 2021-present by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#

import os
import re
import textwrap

import aiofiles
import aiohttp
from PIL import (Image, ImageDraw, ImageEnhance, ImageFilter,
                 ImageFont, ImageOps)
from youtubesearchpython.__future__ import VideosSearch

from config import MUSIC_BOT_NAME, YOUTUBE_IMG_URL


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))


async def gen_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(
                        f"cache/thumb{videoid}.png", mode="wb"
                    )
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(30))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)
        Xcenter = youtube.width / 2
        Ycenter = youtube.height / 2
        x1 = Xcenter - 250
        y1 = Ycenter - 250
        x2 = Xcenter + 250
        y2 = Ycenter + 250
        logo = youtube.crop((x1, y1, x2, y2))
        logo.thumbnail((520, 520), Image.LANCZOS)
        logo = ImageOps.expand(logo, border=15, fill="white")
        background.paste(logo, (50, 100))
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("assets/font2.ttf", 40)
        font2 = ImageFont.truetype("assets/font2.ttf", 70)
        arial = ImageFont.truetype("assets/font2.ttf", 30)
        name_font = ImageFont.truetype("assets/font.ttf", 30)
        para = textwrap.wrap(title, width=32)
        j = 0
        draw.text(
                    (30,10),
                    f"{MUSIC_BOT_NAME}",
                    fill="white",
                    stroke_width=5,
                    stroke_fill="black",
                    font=font5,
        )
        draw.text(
                    (100, 100),
                    "NOW PLAYING",
                    fill="white",
                    stroke_width=8,
                    stroke_fill="black",
                    font=font2,
                )
        for line in para:
                    if j == 1:
                        j += 1
                        draw.text(
                            (120, 280),
                            f"{line}",
                            fill="white",
                            stroke_width=5,
                            stroke_fill="black",
                            font=font,
                        )
                    if j == 0:
                        j += 1
                        draw.text(
                            (120, 220),
                            f"{line}",
                            fill="white",
                            stroke_width=5,
                            stroke_fill="black",
                            font=font,
                        )
        draw.text(
                    (120, 340),
                    f"Views : {views[:23]}",
                    (255, 255, 255),
                    font=arial,
                )
        draw.text(
                    (120, 390),
                    f"Duration : {duration[:23]} Mins",
                    (255, 255, 255),
                    font=arial,
                )
        draw.text(
                    (120, 440),
                    f"Channel : {channel}",
                    (255, 255, 255),
                    font=arial,
                )
        
        draw.text(
                (540,550),
                f"ﮩﮩ٨ـﮩﮩ٨ـﮩ٨ـﮩﮩ٨ـ٨ـﮩﮩ٨ـﮩ٨ـﮩﮩ٨ـ",
                (255, 255, 255),
                font=name_font,
        )
        draw.text(
            (50, 600),
            f"00:55 ─────────────●─────────────────────────────────────────── {duration}",
            (255, 255, 255),
            font=font3,
        
        )
        draw.text(
                (50,650),
                f"Volume: ■■■■■□□□                      ↻      ◁     II    ▷     ↺",
                (255, 255, 255),
                font=font4,
        )
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        background.save(f"cache/{videoid}_{user_id}.png")
        return f"cache/{videoid}_{user_id}.png"
    except Exception as e:
        return YOUTUBE_IMG_URL
