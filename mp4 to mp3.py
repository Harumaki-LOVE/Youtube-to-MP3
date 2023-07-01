import os
from pathlib import Path
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import youtube_dl

url = 'https://www.youtube.com/watch?v=sr--GVIoluU'
ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s',
                                    'postprocessors': [{
                                        'key': 'FFmpegExtractAudio',
                                        'preferredcodec': 'mp3',
                                        'preferredquality': '192',
                                    }]
                                    })

# 動画ダウンロード
with ydl:
    result = ydl.extract_info(
        url,
        download=True
    )

# ファイル名を変更
filename_before1 = url[32:] + 'mp4' + '.mp3'
filename_after1 = url[32:] + '.mp3'
os.rename(filename_before1, filename_after1)
print('処理が完了しました')