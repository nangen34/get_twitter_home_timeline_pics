import webbrowser
import re
import os
import config

# 从config.py中获取文件保存目录
# config.pyから画像の保存パスを取得します
# Get file save path from config.py
IMAGES_DIR = config.PATH

# 从config.py中获取浏览器路径
# config.pyからブラウザがあるフォルダを取得します
# Get file save path from config.py
BROWSER = config.BROSWER

count = 0
print(IMAGES_DIR)
file_list = os.listdir(IMAGES_DIR)
print(file_list)
already_exists_scrren_name_list=[]

for i in range(len(file_list)):
    file_name = file_list[i]
    if re.search("______",file_name):
        print(file_name)
        twitter_screen_name = file_name.split("______")[0]
        if twitter_screen_name in already_exists_scrren_name_list:
            print("twitter id already exists")
            continue
        already_exists_scrren_name_list.append(twitter_screen_name)
        url = "https://twitter.com/%s" % twitter_screen_name

        webbrowser.register('Browser', None, webbrowser.BackgroundBrowser(BROWSER))
        webbrowser.get('Browser').open(url, new=1, autoraise=True)

        count += 1
        if count == 10:
            count = 0
            input("按回车继续 / Press Enter to continue / 続くにはエンターキーを押してください")
