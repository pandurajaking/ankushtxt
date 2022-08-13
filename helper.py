import json
from config import skeleton_url
import subprocess
import datetime
import asyncio
import os
import requests

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if proc.returncode == 1:
        return False
    if stdout:
        return f'[stdout]\n{stdout.decode()}'
    if stderr:
        return f'[stderr]\n{stderr.decode()}'


def parse_json_to_txt(file_name):
    with open(file_name) as f:
        data = json.load(f)
    res = ""
    try:
        details = data["data"]["class_list"]["classes"]
        batch_name = data["data"]["class_list"]["batchName"]
        for i in details:
            name = i["lessonName"]
            id = i["lessonUrl"][0]["link"]
            link = f"{skeleton_url}/{id}"
            res = f"{name}:{link}\n{res}"
        new_file_name = f"{batch_name}.txt"
    except:
        new_file_name = f"{file_name}.txt"
        details = data
        for i in details:
            res = f"{res}\n{i['episode_number']}:{i['file_url']}"

    with open(new_file_name, "w", encoding='utf-8') as f:
            f.write(res.strip())
    return (new_file_name, len(details))


def parse_json_to_html(file_name):
    with open(file_name) as f:
        data = json.load(f)
    batch_name = data["data"]["class_list"]["batchName"]
    details = data["data"]["class_list"]["classes"]
    for i in range( len(details) - 1, -1, -1):
        body_syntax = '''
        <p class="video">
            <span class="video_name">NAME</span>
            <br>
            <a href="LINK" class="youtube" rel="noopener noreferrer" target="_blank">LINK</a>
            </p>
        '''
        name = details[i]["lessonName"]
        id = details[i]["lessonUrl"][0]["link"]
        link = f"{skeleton_url}/{id}"
        body_syntax = body_syntax.replace("NAME", name)
        body_syntax = body_syntax.replace("LINK", link)
        with open(f"{batch_name}.html", "a", encoding='utf-8') as f:
            f.write(body_syntax)
    return (f"{batch_name}.html", len(details))
    

def duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)


def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def time_name():
    date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    return f"{date} {current_time}.mp4"


def parse_vid_info(info):
    info = info.strip()
    info = info.split("\n")
    new_info = []
    temp = []
    for i in info:
        i = str(i)
        if "[" not in i and '---' not in i:
            while "  " in i:
                i = i.replace("  ", " ")
            i.strip()
            i = i.split("|")[0].split(" ",2)
            try:
                if "RESOLUTION" not in i[2] and i[2] not in temp and "audio" not in i[2]:
                    temp.append(i[2])
                    new_info.append((i[0], i[2]))
            except:
                pass
    return new_info


async def download_video(url, name, ytf="bestvideo[height<=720]"):
    cmd = f'yt-dlp -o "{name}" -f "{ytf}+bestaudio" "{url}"'
    k = await run(cmd)
    if not k:
        cmd = f'yt-dlp -o "{name}" "{url}"'
        await run(cmd)

    if os.path.isfile(name):
        return name
    elif os.path.isfile(f"{name}.webm"):
        return f"{name}.webm"
    name = name.split(".")[0]
    if os.path.isfile(f"{name}.mkv"):
        return f"{name}.mkv"
    elif os.path.isfile(f"{name}.mp4"):
        return f"{name}.mp4"

    return name

def old_download(url, file_name, chunk_size = 1024 * 10):
    if os.path.exists(file_name):
        os.remove(file_name)
    r = requests.get(url, allow_redirects=True, stream=True)
    with open(file_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                fd.write(chunk)
    return file_name