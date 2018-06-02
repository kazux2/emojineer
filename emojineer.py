import cv2
import json
from os import listdir
from os.path import isfile, join
import numpy as np
from operator import itemgetter

dir_path = 'emojineer/target_img'
target_file_name = '7-eleven_logo.png'

target_img = cv2.imread('{}/{}'.format(dir_path, target_file_name))
print(target_img.shape)
height, width = target_img.shape[:2]

convert_density = 480

h_number = height // convert_density
w_number = width // convert_density

#git

'''cut target img'''
cut_target_img = []
for h in range(h_number):
	horizon_cut = []
	for w in range(w_number):
		cut_piece = target_img[h*convert_density:(h+1)*convert_density, w*convert_density:(w+1)*convert_density]
		cut_piece_1x1 = cv2.resize(cut_piece, (1,1))
		horizon_cut.append(cut_piece_1x1)
	cut_target_img.append(horizon_cut)


whiten_emoji_path = 'data/whiten_emoji_apple'

whiten_emoji_file_names = [f for f in listdir(whiten_emoji_path) if isfile(join(whiten_emoji_path, f))]

with open('data/whiten_emoji_1x1_rgb.json', 'r') as f:
	whiten_emoji_1x1_rgb = json.load(f)





'''calc nearest emojis'''
emojis = []
for h in range(h_number):
	horizon_emoji = []
	for w in range(w_number):
		dist_candidate = {}
		for w_emoji_name in whiten_emoji_file_names:

			if not w_emoji_name == '.DS_Store':
				emoji_rgb = np.array(whiten_emoji_1x1_rgb[w_emoji_name])
				cut_piece_rgb = cut_target_img[h][w]
				distance = (emoji_rgb[0][0][0]-cut_piece_rgb[0][0][0])**2\
				           + (emoji_rgb[0][0][1]-cut_piece_rgb[0][0][1])**2\
				           + (emoji_rgb[0][0][2]-cut_piece_rgb[0][0][2])**2
				dist_candidate[w_emoji_name] = distance
		horizon_emoji.append(min(dist_candidate.items(), key=itemgetter(1))[0])
	emojis.append(horizon_emoji)

with open('emojineer/calc_result/calc_result50', 'w') as f:
	json.dump(emojis, f, indent=2)



'''concatinate emojis'''

with open('emojineer/calc_result/calc_result50', 'r') as f:
	emojis = json.load(f)

vertical_imgs = []
for h in range(h_number):
	horison_imgs = []
	for w in range(w_number):
		img = cv2.imread('{}/{}'.format(whiten_emoji_path, emojis[h][w]))
		horison_imgs.append(img)
	im_v = cv2.hconcat(horison_imgs)
	vertical_imgs.append(im_v)
converted_img = cv2.vconcat(vertical_imgs)


cv2.imwrite('emojineer/converted_img/conv_img_{}.png'.format(convert_density), converted_img)
# cv2.imshow('name', converted_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
