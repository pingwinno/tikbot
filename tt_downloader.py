import os
import uuid

import requests
import yt_dlp


def get_video(url):
    path = f'{str(uuid.uuid4())}.mp4'
    ydl_opts = {
        'format': 'best',
        'outtmpl': path,
        'noplaylist': True,
        'quiet': False,
        'extractor_args': {'tiktok': {'webpage_download': True}},
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }

    response = requests.get(url, allow_redirects=True)

    # Get the final URL
    final_url = response.url

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([final_url])
        print(f"\nVideo successfully downloaded: ")
    return path


def remove_video(name):
    print(f'removing video {name}')
    os.remove(name)
