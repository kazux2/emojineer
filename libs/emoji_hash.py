
import json
import time
import os, sys
import numpy as np
from operator import itemgetter

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open('{}/{}'.format(pardir, 'data/whiten_emoji_1x1_rgb.json'), 'r') as f:
	whiten_emoji_1x1_rgb = json.load(f)

num_wemoji_dict = {}
wemoji_num_dict = {}
idx = 0
for key in whiten_emoji_1x1_rgb.keys():
	num_wemoji_dict[idx] = key
	wemoji_num_dict[key] = idx
	idx += 1


# need these index_to_id/id_to_index file for emojineer.py when
with open('{}/{}'.format(pardir, 'data/num_wemoji_dict.json'), 'w') as f:
	json.dump(num_wemoji_dict, f, indent=2)

with open('{}/{}'.format(pardir, 'data/wemoji_num_dict.json'), 'w') as f:
	json.dump(wemoji_num_dict, f, indent=2)

'''
all_rgb_dict = {
'000000000':[0, 0, 0],
'000000001':[0, 0, 5],
...
'255255255:[255, 255, 255]
}
'''
all_rgb_dict = {}

for r in range(0, 256, 5):
	for g in range(0, 256, 5):
		for b in range(0, 256, 5):
			_r = '{0:03d}'.format(r)
			_g = '{0:03d}'.format(g)
			_b = '{0:03d}'.format(b)
			dict_key = '{}{}{}'.format(_r, _g, _b)
			all_rgb_dict[dict_key] = [r, g, b]
			print(dict_key)
	# 		break
	# 	break
	# break

'''
rgb_emoji_dict = {
'000000000':"w_tiger-face_1f42f.png",
...
'255255255:"_white.png"
}
'''


for rgb_key, rgb_array in all_rgb_dict.items():
	rgb_emoji_dict = []
	print('calc for {}'.format(rgb_key))
	rgb_ndarray = np.array(rgb_array)

	emoji_distance_dict = {}
	for emoji_name, emoji_rgb in whiten_emoji_1x1_rgb.items():
		nd_emoji_rgb = np.array(emoji_rgb)

		distance = (nd_emoji_rgb[0][0][0] - rgb_ndarray[0]) ** 2 \
				   + (nd_emoji_rgb[0][0][1] - rgb_ndarray[1]) ** 2 \
				   + (nd_emoji_rgb[0][0][2] - rgb_ndarray[2]) ** 2
		emoji_distance_dict[emoji_name] = distance

	# save top five similar emoji NUM as file
	rgb_emoji_dict = [ wemoji_num_dict[i[0]] for i
					   in sorted(emoji_distance_dict.items(), key=itemgetter(1))[:5]
					   ]

	with open('{}/{}/{}.json'.format(pardir, 'data/w1x1_hash_dicts_0_256_5/', rgb_key), 'w') as f:
		json.dump(rgb_emoji_dict, f)

	# for DB use
	# rgb_emoji = sorted(emoji_distance_dict.items(), key=itemgetter(1))[0][0]
	# print(rgb_emoji)
	# from libs.db_access import W1x1RGBtoEmojiname
	#
	# record_num, created = W1x1RGBtoEmojiname.get_or_create(rgb_value=int(rgb_key), emoji_file_name=rgb_emoji)
	# print(record_num, "th record created:", created)







