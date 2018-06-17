'''
ここ全然理解してない

2値化閾値を使ったマスキング
https://postd.cc/image-processing-101/
'''


import cv2
from os import listdir
from os.path import isfile, join, splitext

dir_path = 'data/emoji_apple'
save_path = 'data/whiten_emoji_apple'

file_names = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]



for file_name in file_names:

    root, ext = splitext(file_name)
    if not ext in ['.png', '.jpeg', '.jpg']:
        continue

    img_4chan = cv2.imread('{}/{}'.format(dir_path, file_name), cv2.IMREAD_UNCHANGED)
    img_color = cv2.imread('{}/{}'.format(dir_path, file_name), cv2.IMREAD_COLOR)

    # get mask of pixels that are in blue range
    alpha_channel = img_4chan[:,:,3]
    mask = alpha_channel

    # inverse mask to get parts that are not blue
    mask_inverse= cv2.bitwise_not(mask)

    # convert single channel mask back into 3 channels
    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

    # perform bitwise and on mask to obtain cut-out image that is not blue
    masked_upstate = cv2.bitwise_and(img_color, mask_rgb)

    # replace the cut-out parts with white
    masked_replace_white = cv2.addWeighted(masked_upstate, 1,
                                           cv2.cvtColor(mask_inverse, cv2.COLOR_GRAY2RGB), 1, 0)

    cv2.imwrite('{}/w_{}'.format(save_path, file_name), masked_replace_white)
