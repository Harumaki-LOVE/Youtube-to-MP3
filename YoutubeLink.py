import os
from pathlib import Path
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class YoutubeChannelVideoScraper(object):
    def __init__(self, user_name, csv_file_name):
        self.youtube_url = "https://www.youtube.com"
        self.user_name = user_name #usernameはYoutuber名
        self.csv_file_name = csv_file_name 
        #csvファイルのpath=カレントディレクトリ+csvファイル名
        self.csv_file_path = os.path.join(os.getcwd(), self.csv_file_name+'.csv') 
        #csvファイルのpath=カレントディレクトリ/csvファイル名
        self.channel_videos_url = os.path.join(self.youtube_url,self.user_name, 'videos')
        self.titles = []
        self.video_urls = []

    def run(self):
        #ソースの取得
        self.get_page_source()
        #動画とURLの抽出
        self.parse_video_title_and_url()
        #データの保存
        self.save_as_csv_file()

    def get_page_source(self):
        '''
        YoutubeChannelページの
        最下部までスクロールしたページソースを取得
        '''
        # ブラウザ操作の準備
        self.driver = webdriver.Edge(executable_path="C:\dev\msedgedriver.exe")
        self.driver.get(self.channel_videos_url)
        self.current_html = self.driver.page_source

        # 動画一覧要素へ移動
        element = self.driver.find_element_by_xpath('//*[@class="style-scope ytd-page-manager"]')
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.perform()
        actions.reset_actions()

        # 最下部までスクロールしたソースを取得
        while True:
            for j in range(100):
                actions.send_keys(Keys.PAGE_DOWN)
            actions.perform()
            sleep(3)
            html = self.driver.page_source
            if self.current_html != html:
                self.current_html=html
            else:
                break

    def parse_video_title_and_url(self):
        '''
        タイトルと動画URLを抽出
        '''
        soup = BeautifulSoup(self.current_html, 'html.parser')
        for i in soup.find_all("a"):
            title = (i.get("title"))
            url = (i.get("href"))
            if title is None:
                continue
            elif url is None:
                continue
            if "/watch?v=" in url:
                self.titles.append(title)
                self.video_urls.append(url)


    def save_as_csv_file(self):
        '''
        CSVファイルとして保存
        '''
        data = {
         "title": self.titles,
         "url": self.video_urls
        }
        pd.DataFrame(data).to_csv(self.csv_file_path,index=False)


if __name__ == "__main__":
    youtuber_name = "Vaundy"
    scraper = YoutubeChannelVideoScraper(user_name=youtuber_name, csv_file_name=youtuber_name)
    scraper.run()