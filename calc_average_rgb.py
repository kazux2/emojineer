
'''
色の類似度はユークリッド距離がベスト
https://spphire9.wordpress.com/2011/03/18/%E8%89%B2%E3%81%AE%E9%A1%9E%E4%BC%BC%E5%BA%A6/

1x1でおけ
http://shokai.org/blog/archives/4961

'''

''' resize -> 1x1, create rgb json
{
'emoji_nameA':[r, g, b],
'emoji_nameB':[r, g, b],
'emoji_nameC':[r, g, b],
...
}
'''


def show_image(cv2image_list):
    for cv2img in cv2image_list:
        cv2.imshow('name', cv2img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def imread_color(path):
    return cv2.imread(path, cv2.IMREAD_COLOR)

import cv2
import json
from os import listdir
from os.path import isfile, join, splitext
import numpy as np
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN


dir_path = 'data/whiten_emoji_apple'

file_names = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
print(file_names[0])

whiten_emoji_1x1_rgb_dict = {}

for file_name in file_names:

    root, ext = splitext(file_name)
    if not ext in ['.png', '.jpeg', '.jpg']:
        continue

    img = cv2.imread('{}/{}'.format(dir_path, file_name), cv2.IMREAD_COLOR)

    # impplemented from Daichi/fix_color #18
    img_ave = np.zeros(3)
    img_ave[0] = np.sum(img[:, :, 0]) / (72 * 72)
    img_ave[1] = np.sum(img[:, :, 1]) / (72 * 72)
    img_ave[2] = np.sum(img[:, :, 2]) / (72 * 72)

    img_ave[0] = Decimal(str(img_ave[0])).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
    img_ave[1] = Decimal(str(img_ave[1])).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
    img_ave[2] = Decimal(str(img_ave[2])).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
    img_ave = img_ave.reshape(1, 1, 3)

    # img_resized = cv2.resize(img, (1,1))
    whiten_emoji_1x1_rgb_dict[file_name] = img_ave.tolist()

with open('data/whiten_emoji_1x1_rgb.json', 'w') as f:
    json.dump(whiten_emoji_1x1_rgb_dict, f, indent=2)

