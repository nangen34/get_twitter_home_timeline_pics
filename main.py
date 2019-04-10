#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import re
import config
import os
import time
import urllib
from twython import Twython

# 从config.py中获取文件保存目录
# Get file save path from config.py
IMAGES_DIR = config.PATH
# 从config.py中获取定时器的时间间隔
# Get the timer interval from config.py
TIMER = config.TIMER
# 从config.py中获取Twitter认证信息
# Get your Twitter key or token etc
CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
ATK = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET

# NUM_PAGES = 5
# TWEET_PER_PAGE = 200

name_list = []

class TwitterImageDownloader(object):

    def __init__(self):
        super(TwitterImageDownloader, self).__init__()
        self.twitter = Twython(app_key=CK, app_secret=CS, oauth_token=ATK, oauth_token_secret=ATS)


    # def read_ids(self):
    #     ids_all = [line.replace('@', '') for line in SCREEN_NAMES.splitlines() if line]
    #     ids = sorted(list(set(ids_all)))
    #     return ids

    def get_timeline(self):
        url_listx = []
        name_listx = []
        try:
            tw_result = self.twitter.get_home_timeline(count=200)
            time.sleep(5)
        except Exception as e:
            print("timeline get error ", e)
        else:
            for result in tw_result:
                # if tweet contain a picture, get it.
                if 'extended_entities' in result:
                    media = result['extended_entities']['media']
                    print("tweet contain", len(media), ' picture(s)')
                    url_list_multi = []
                    for url in media:
                        url_list_multi.append(url['media_url'])
                    url_listx.append(url_list_multi)

                    # judge if the tweet is RT or not so we can get the correct twitter id.
                    if 'retweeted_status' in result:
                        # print("yes rt")
                        name = result['retweeted_status']['user']['screen_name']
                        name_listx.append(name)
                        # print(name)
                    else:
                        # print("not rt")
                        name = result['user']['screen_name']
                        name_listx.append(name)
                else:
                    print("no imgs")

        return url_listx,name_listx

    def create_folder(self, save_dir):
        try:
            os.mkdir(save_dir)
        except Exception as e:
            print
            'cannot make dir', e
        # 获取文件列表 以便判断是否有重复图片
        # Get a list of files to determine if there are duplicate images
        file_list = os.listdir(save_dir)
        return file_list

    def get_file(self, url, file_list, save_dir, name_listx, urll, j):
        # print(url)
        for i in range(len(url)):
            url_real = url[i]

            # 截取图片文件名 例如：https://pbs.twimg.com/media/D3uPR1cU0AAuOW9.jpg
            #———————————————————————————こ↑こ↓————
            # get file name of pics. For example：https://pbs.twimg.com/media/D3uPR1cU0AAuOW9.jpg
            # ——————————————————————————— ↑____this part____↑
            file_name_judge = url_real[url_real.rfind('/') + 1:]

            #拼接成储存用的最终文件名 例如00unit(作者名)______D3rIFukUIAA7EwF.jpg(文件名)
            #Create the final file name. For example:00unit(twitter id)______D3rIFukUIAA7EwF.jpg(file names of pics)
            file_name = name_listx[j] + "______" + file_name_judge
            url_large = '%s:large' % (url_real)

            #判断图片是否重复
            #determine if there are duplicate images
            result = None
            for i in file_list:
                result = re.search(file_name_judge, i)
                if result != None:
                    break
            # print(result)
            if result == None:
                save_path = os.path.join(save_dir, file_name)
                try:
                    print
                    "download", url_large
                    print("download start")
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
                    # time.sleep(0.5)
            else:
                print("file already exists.  skip", file_name)

    #下载图片
    #download pics
    def download(self):
        save_dir = os.path.join(IMAGES_DIR)
        file_list = self.create_folder(save_dir)

        url_list,name_list = self.get_timeline()
        for j, url in enumerate(url_list):
            self.get_file(url, file_list, save_dir,name_list, url_list, j)


def main():
    print("started")
    tw = TwitterImageDownloader()
    tw.download()
    print("finished")

    #定时器
    global timer
    timer = threading.Timer(TIMER, main)
    timer.start()


if __name__ == '__main__':
    main()
    timer = threading.Timer(TIMER, main)
    timer.start()