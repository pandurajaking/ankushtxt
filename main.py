#  MIT License
#
#  Copyright (c) 2019-present Dan <https://github.com/delivrance>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE
from FastTelethonhelper import fast_upload

from telethon.tl.types import DocumentAttributeVideo


import requests
import json
import subprocess
from pyrogram import Client,filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
import pyrogram
from pyrogram import Client, filters
import tgcrypto
from p_bar import progress_bar
from subprocess import getstatusoutput
import helper
import logging
import time
import aiohttp
import asyncio
import aiofiles
from pyrogram.types import User, Message
import sys
import re
import os


API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
NAME = os.environ.get("NAME")

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, sleep_threshold=120)


@bot.on_message(filters.command(["start"])& ~filters.edited)
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("Hello im txt file downloader\nPress /download to download links listed in a txt file in the format **Name:link**\n\nBot made by BlackOuT")

@bot.on_message(filters.command(["cancel"]))
async def cancel(_, m):
    editable = await m.reply_text("Canceling All process Plz wait")
    global cancel
    cancel = True
    await editable.edit("cancled")
    return
@bot.on_message(filters.command("restart"))
async def restart_handler(_, m):
    await m.reply_text("Restarted!", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["download"])& ~filters.edited)
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("Send txt file**")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/"

    try:    
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split(":", 1))
        os.remove(x)
        # print(len(links))
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    editable = await m.reply_text(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **0**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text


    try:
        arg = int(raw_text)
    except:
        arg = 0
    
    
    editable = await m.reply_text("**Enter Batch Name**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text0 = input0.text
    
    editable7= await m.reply_text("**Downloaded By : **")
    input7 = Message = await bot.listen(editable.chat.id)
    raw_te = input7.text
    
    await m.reply_text("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text

    editable4= await m.reply_text("Now send the **Thumb url**\nEg : ```https://telegra.ph/file/d9e24878bd4aba05049a1.jpg```\n\nor Send **no**")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    thumb = input6.text
    
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"
        
    if raw_text =='0':
        count =1
    else:       
        count =int(raw_text) 
    try:
        for i in range(arg, len(links)):
            try:
                if cancel == True:
                    await m.reply_text("Process canceled")
                    return
                url = links[i][1]
                name = links[i][0].replace("\t", "")
                Show = f"**Downloading:-**\n\n**Name :-** `{name}\nQuality - {raw_text2}`\n\n**Url :-** `{url}`\n\n"
                prog = await m.reply_text(Show)
                cc = f"**{count}) Title :** {name}\n\n**Quality :** {raw_text2}\n**Batch :** {raw_text0}\n**𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗱 𝗕𝘆 :** {raw_te}\n**𝗕𝗼𝘁 𝗢𝘄𝗻𝗲𝗿 : 𝗕𝗹𝗮𝗰𝗸𝗢𝘂𝗧 (•̪●)=︻╦̵̵̿╤── **\n**𝗣𝗹𝘇 𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗯𝗲 : https://www.youtube.com/channel/UC7udfRGdD_QoCg-OnSooGAA**"

                filename = f"{name[:60]}.mp4"
                k = await helper.download_video(url, filename)
                filename = k
                filename = await helper.download_video(url, file_name, vid_id)
                res_file = await fast_upload(bot, filename, r)
 
                subprocess.call(f'ffmpeg -i "{filename}" -ss 00:00:01 -vframes 1 "{filename}.jpg"', shell=True)
                reply = await m.reply_text(f"Uploading - ```{name}```")
                try:
                    if thumb == "no":
                        thumbnail = f"{filename}.jpg"
                    else:
                        thumbnail = thumb
                except Exception as e:
                    await m.reply_text(str(e))

                try:
                    dur = int(helper.duration(filename))
                    await bot.send_message(
                        event.chat_id, 
                        f"{caption}", 
                        file=res_file, 
                        force_document=False, 
                        thumb=thumbnail, 
                        supports_streaming=True,
                        progress=progress_bar,progress_args=(reply,start_time),
                        attributes=[DocumentAttributeVideo(
                            duration=dur, 
                            w=1260, 
                            h=720, 
                            supports_streaming=True
                        )]
                    )

                except:
                    await bot.send_message(event.chat_id,"There was an error while uploading file as streamable so, now trying to upload as document.")
                    await bot.send_message(
                        event.chat_id, 
                        f"`{caption}`", 
                        file=res_file, 
                        force_document=True,
                    )

                os.remove(filename)
                os.remove(f"{filename}.jpg")

                await r.delete()   
        
            except Exception as e:
                print(e)
                pass
          
    except Exception as e:
        await m.reply_text(str(e))
    await m.reply_text("Done")

bot.run()

@bot.on_message(filters.command(["sthumb"])& ~filters.edited)
async def account_login(bot: Client, event: Message):

    x = await event.get_reply_message()
    thumb = await bot.download_media(x.photo)
    with open(thumb, "rb") as f:
        pic = f.read()
    with open("thumb.png", "wb") as f:
        f.write(pic)
    await event.reply("Set as default thumbnail")


@bot.on_message(filters.command(["cthumb"])& ~filters.edited)
async def account_login(bot: Client, event: Message):
    with open("thumb.png", "w") as f:
        f.write("")
    os.remove("thumb.png")
    await event.reply("cleared thumbnail")


@bot.on_message(filters.command(["vthumb"])& ~filters.edited)
async def account_login(bot: Client, event: Message):
    try:
        await event.reply("current default thumbnail", file="thumb.png")
    except:
        await event.reply("No default thumbnail set")



@bot.on_message(filters.command(["cancel"]))
async def cancel(_, m):
    editable = await m.reply_text("Canceling All process Plz wait")
    global cancel
    cancel = True
    await editable.edit("cancled")
    return


@bot.on_message(filters.command(["download1"])& ~filters.edited)
async def account_login(bot: Client, event: Message):

    global cancel
    cancel = False
    try:
        arg = int(event.raw_text.split(" ")[1])
        arg -= 1
    except:
        arg = 0
    try:
        txt_file = await event.get_reply_message()
        x = await bot.download_media(txt_file)
        with open(x) as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split(":", 1))
        os.remove(x)
    except:
        await event.reply("Invalid file input.")
        os.remove(x)
        return
    for i in range(arg, len(links)):
        try:
            if cancel == True:
                await event.reply("Process canceled")
                return
            url = links[i][1]
            name = links[i][0].replace("\t", "")
            filename = f"{name[:60]}.mp4"
            r = await event.reply(f"`Downloading...\n{name[:60]}\n\nfile number: {i+1}`")
            caption =  f"`{name[:60]}\n\nfile number: {i+1}`"
            k = await helper.download_video(url, filename)
            filename = k
            res_file = await fast_upload(bot, filename, r)
 
            subprocess.call(f'ffmpeg -i "{filename}" -ss 00:00:01 -vframes 1 "{filename}.jpg"', shell=True)

            dur = int(helper.duration(filename))
            try:
                await bot.send_message(
                    event.chat_id, 
                    caption, 
                    file=res_file, 
                    force_document=False, 
                    thumb=thumbnail, 
                    supports_streaming=True, 
                    attributes=[DocumentAttributeVideo(
                        duration=dur, 
                        w=1260, 
                        h=720, 
                        supports_streaming=True
                    )]
                )
            except:
                await bot.send_message(
                    event.chat_id,
                    "There was an error while uploading file as streamable so, now trying to upload as document."
                )
                await bot.send_message(
                    event.chat_id, 
                    caption, 
                    file=res_file, 
                    force_document=True,
                )
            os.remove(filename)
            os.remove(f"{filename}.jpg")
            await r.delete()

        
        except Exception as e:
            print(e)
            pass
          
          
@bot.on_message(filters.command(["upload"])& ~filters.edited)
async def account_login(bot: Client, event: Message):
    
    arg = event.raw_text.split(" ", maxsplit = 1)[1]
    arg = arg.split("|")
    if len(arg) == 1:
        file_name = arg[0].split("/")[-1]
        caption = ''
    elif len(arg) == 2:
        file_name = arg[1].strip()
        caption = arg[1].strip()
    else:
        file_name = arg[1].strip()
        caption = arg[2].strip()

    cmd = f'yt-dlp -F "{arg[0]}"'
    k = await helper.run(cmd)
    out = helper.parse_vid_info(str(k))
    print(out)
    buttons = []

    if 'unknown' in out[0][1]:
        r = await event.reply("downloading.")
        f = helper.old_download(arg[0], file_name)
        res_file = await fast_upload(bot, f, r)
        await bot.send_message(
            event.chat_id, 
            f"`{caption}`", 
            file=res_file, 
            force_document=True,
        )
        return

    for i in out:
        if 'youtu' in arg[0]:
            print(i[1])
            x = i[1].split()[0].split("x")[-1]
            buttons.append([Button.inline(i[1], data=f"id:bestvideo[height<={x}][ext=mp4]")])
        else:
            buttons.append([Button.inline(i[1], data=f"id:{i[0]}")])
    await bot.send_message(event.chat_id, f"`Name: {file_name}`\n`Caption: {caption}`\n`Url: {arg[0]}`", buttons=buttons)
    
@bot.on_message(filters.command(["txt"])& ~filters.edited)
async def account_login(bot: Client, event: Message):

    try:
        x = await event.get_reply_message()
        json_file = await bot.download_media(x)
        res, count = helper.parse_json_to_txt(json_file)
        await event.reply(f"{count} links detected." ,file=res)
        os.remove(json_file)
        os.remove(res)
    except Exception as e:
        print(e)
        await event.reply("Invalid Json file input.")

@bot.on_message(filters.command(["html"])& ~filters.edited)
async def account_login(bot: Client, event: Message):

    try:
        x = await event.get_reply_message()
        json_file = await bot.download_media(x)
        res, count = helper.parse_json_to_html(json_file)
        await event.reply(f"{count} links detected." ,file=res)
        os.remove(json_file)
        os.remove(res)
    except Exception:
        await event.reply("Invalid Json file input.")

@bot.on_message(events.CallbackQuery(pattern=b"id:"))
async def account_login(bot: Client, event: Message):
    r = await event.reply("Trying to download....")
    data = event.data.decode('utf-8')
    data = data.split(":")
    msg = await bot.get_messages(event.chat_id, ids=event.message_id)
    await msg.edit(buttons=None)
    msg = msg.raw_text.split("\n")
    file_name = msg[0].replace("Name: ", "")
    caption = msg[1].replace("Caption: ", "")
    url = msg[2].replace("Url: ", "") 
    vid_id = (data[1])
    filename = await helper.download_video(url, file_name, vid_id)
    res_file = await fast_upload(bot, filename, r)
    if not os.path.isfile("thumb.png"):
        subprocess.call(f'ffmpeg -i "{filename}" -ss 00:00:01 -vframes 1 "{filename}.jpg"', shell=True)
        thumbnail = f"{filename}.jpg"
    else:
        thumbnail = "thumb.png"
    try:
        dur = int(helper.duration(filename))
        await bot.send_message(
            event.chat_id, 
            f"{caption}", 
            file=res_file, 
            force_document=False, 
            thumb=thumbnail, 
            supports_streaming=True, 
            attributes=[DocumentAttributeVideo(
                duration=dur, 
                w=1260, 
                h=720, 
                supports_streaming=True
            )]
        )

    except:
        await bot.send_message(
            event.chat_id,
            "There was an error while uploading file as streamable so, now trying to upload as document."
        )
        await bot.send_message(
            event.chat_id, 
            f"`{caption}`", 
            file=res_file, 
            force_document=True,
        )

    os.remove(filename)
    os.remove(f"{filename}.jpg")

    await r.delete()   


bot.run()

