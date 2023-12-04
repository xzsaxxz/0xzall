from __future__ import unicode_literals

import os

import requests
import yt_dlp
from pyrogram import Client, filters
from YukkiMusic import app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL


ydl_opts = {
    "format": "best",
    "keepvideo": True,
    "prefer_ffmpeg": False,
    "geo_bypass": True,
    "outtmpl": "%(title)s.%(ext)s",
    "quite": True,
}



@app.on_message(
    filters.command(["يوت","/song","بحث"],""))
def song(client, message):

    message.delete()
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chutiya = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"

    query = ""
    for i in message.command[1:]:
        query += " " + str(i)
    print(query)
    m = message.reply("**» جاري البحث ...**")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        # print(results)
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)

        duration = results[0]["duration"]
        results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "**~ للاسف ما اثرت على شي تأكد من كتابة اسم الفنان مع الاغنية**"
        )
        print(str(e))
        return
    m.edit("**» جاري التحميل**...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"**𝙹𝙾𝙸𝙽 ››** [ᴄʜᴀɴɴᴇʟ](t.me/FH_KP)\n**𝙿𝙾𝚆𝙴𝚁𝙴𝙳 𝙱𝚈 ››** @{app.username}"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60
        message.reply_audio(
            audio_file,
            caption=rep,
            thumb=thumb_name,
            title=title,
            duration=dur,
        )
        m.delete()
    except Exception as e:
        m.edit(
            f"**» حدث خطأ أثناء البحث حاول مره اخرى**"
        )
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

                
            
        
            

__mod_name__ = "⚡Sᴏɴɢ⚡"
__help__ = """
/song ᴛᴏ  ᴅᴏᴡɴʟᴏᴀᴅ   ᴀɴʏ  sᴏɴɢ 
/music ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴀɴʏ  sᴏɴɢ

☆............𝙱𝚈 » [ᯓ 𝘼𝙇𓄂𝙈𝘼𝙀𝙎𝙏𝙍𝙊⚝➣⃟𝙈ِ°亗™↝⸀🇾🇪˼](https://t.me/FH_ME)............☆"""
