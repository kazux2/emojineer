import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib import error, request

'''save emojipedia's html'''
r = requests.get("https://emojipedia.org/apple/")
soup = BeautifulSoup(r.content, 'html.parser')
with open('data/emojipedia_apple.html', "w") as f:
    f.write(soup.prettify())


'''save image url list'''
with open('data/emojipedia_apple.html', "r") as f:
    soup = BeautifulSoup(f, 'html.parser')


emoji_grid = soup.find("div", {"class": "content"}).find("ul", {"class": "emoji-grid"})
first_20_images = emoji_grid.find_all("img")

img_url_list = []


for img in first_20_images:
    if img['src'] == '/static/img/lazy.svg':
        img_url_list.append(img['data-src'])
    else:
        img_url_list.append(img['src'])


with open('data/img_url_list', "w") as f:
    json.dump(img_url_list, f, indent=2)


'''download image'''
with open('data/img_url_list', "r") as f:
    img_url_list_load = json.load(f)
# print(img_url_list_load)

download_dir = 'data/emoji_apple'
sleep_time_sec = 1


def download_image(url, dst_path):
    try:
        data = request.urlopen(url).read()
        with open(dst_path, mode="wb") as f:
            f.write(data)
    except error.URLError as e:
        print(e)


for url in img_url_list_load:
    filename = os.path.basename(url)
    dst_path = os.path.join(download_dir, filename)
    print(url, dst_path)
    download_image(url, dst_path)



