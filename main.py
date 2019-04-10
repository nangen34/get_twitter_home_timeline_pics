#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import re
import config
import os
import time
import urllib
from twython import Twython

u"""
ツイッターで投稿された画像を一括でダウンロードする
"""

# 画像を保存するディレクトリ(予め作成しておく)
# 各ユーザの画像は、./images/screen_name/ 内に保存される
IMAGES_DIR = './'
CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
ATK = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
# Twitter 認証関係 https://dev.twitter.com/apps
# Consumer key
# CK = 'Consumer keyをここに記入'
# # Consumer secret
# CS = 'Consumer secretをここに記入'
# # Access token
# ATK = 'Access tokenをここに記入'
# # Access token secret
# ATS = 'Access token secretをここに記入'

# 取得するツイート数の最大値の設定(以下の2つの値の積)
NUM_PAGES = 5  # 取得するページ数
TWEET_PER_PAGE = 200  # 1ページあたりのツイート数(最大200)

# 画像をダウンロードするユーザのスクリーン名を1行に1人ずつ記入する(@の有無は問わない)
SCREEN_NAMES = '''
nanyuan_342
'''
name_list = []

class TwitterImageDownloader(object):
    u"""Twitterから画像をダウンロードする"""

    def __init__(self):
        super(TwitterImageDownloader, self).__init__()
        self.twitter = Twython(app_key=CK, app_secret=CS, oauth_token=ATK, oauth_token_secret=ATS)


    def read_ids(self):
        ids_all = [line.replace('@', '') for line in SCREEN_NAMES.splitlines() if line]
        ids = sorted(list(set(ids_all)))
        return ids

    def get_timeline(self):
        max_id = ''
        url_listx = []
        name_listx = []
        # for i in range(NUM_PAGES):
        try:
            # print
            # 'getting timeline : @', screen_name, (i + 1), 'page'
            tw_result = self.twitter.get_home_timeline(count=200)
            # tw_result = (
            #     self.twitter.get_user_timeline(screen_name=screen_name, count=TWEET_PER_PAGE, max_id=max_id)
            #     if max_id else self.twitter.get_user_timeline(screen_name=screen_name, count=TWEET_PER_PAGE))
            time.sleep(5)
        except Exception as e:
            print
            "timeline get error ", e
            # break
        else:
            for result in tw_result:
                # print(result)
                if 'extended_entities' in result:
                    # if 'media' in result['extended_entities']:
                    media = result['extended_entities']['media']
                    print("len", len(media))
                    url_list_multi = []
                    for url in media:
                        url_list_multi.append(url['media_url'])
                    url_listx.append(url_list_multi)
                    if 'retweeted_status' in result:
                        # print("yes rt")
                        name = result['retweeted_status']['user']['screen_name']
                        name_listx.append(name)
                    else:
                        # print("not rt")
                        name = result['user']['screen_name']
                        name_listx.append(name)
                else:
                    print("no imgs")
            # print(len(url_listx),url_listx)
            # print(len(name_listx),name_listx)
        # if len(tw_result) < TWEET_PER_PAGE:
        #     break
        return url_listx,name_listx

    def create_folder(self, save_dir):
        try:
            os.mkdir(save_dir)
        except Exception as e:
            print
            'cannot make dir', e
        # 生成文件列表
        file_list = os.listdir(save_dir)
        return file_list

    def get_file(self, url, file_list, save_dir, name_listx, urll, j):
        # print(url)
        for i in range(len(url)):
            url_real = url[i]
            # print('real',url_real)
            file_name_judge = url_real[url_real.rfind('/') + 1:]
            file_name_file = url_real[url_real.rfind('.') + 1:]
            # print(file_name_judge)
            # print(name_listx)
            file_name = name_listx[j] + "______" + file_name_judge + "." + file_name_file
            url_large = '%s:large' % (url_real)
            result = None
            for i in file_list:
                # print(file_name_judge, "xxxx", i)
                result = re.search(file_name_judge, i)
                if result != None:
                    break
            print(result)
            if result == None:
                save_path = os.path.join(save_dir, file_name)
                try:
                    print
                    "download", url_large
                    print("no problem")
                    url_req = urllib.request.urlopen(url_large)
                except Exception as e:
                    print(e)
                    continue
                else:
                    print("saving", str(j), "//", len(urll))
                    img_read = url_req.read()
                    img = open(save_path, 'wb')
                    img.write(img_read)
                    img.close()
                    time.sleep(0.5)
            else:
                print("file already exists", file_name)


    def download(self):
        screen_name_list = self.read_ids()
        num_users = len(screen_name_list)
        # print(screen_name_list)
        # for i, screen_name in enumerate(screen_name_list):
        save_dir = os.path.join(IMAGES_DIR, 'resultx')
        file_list = self.create_folder(save_dir)

        url_list,name_list = self.get_timeline()
        # print(name_list)
        # print(url_list)
        num_urls = len(url_list)
        for j, url in enumerate(url_list):
            self.get_file(url, file_list, save_dir,name_list, url_list, j)


def main():
    print("started")
    tw = TwitterImageDownloader()
    tw.download()
    print("finished")

    global timer
    timer = threading.Timer(600, main)
    timer.start()


if __name__ == '__main__':
    main()
    timer = threading.Timer(600, main)
    timer.start()