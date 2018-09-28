
import json
import pickle
import time
import os, sys
import numpy as np
from operator import itemgetter



'''
creating all_rgb

all_rgb = {
'000000000':[0, 0, 0],
'000000001':[0, 0, 5],
...
'255255255:[255, 255, 255]
}
'''

all_rgb = {}

step = 20
for r in range(0, 256, step):
	for g in range(0, 256, step):
		for b in range(0, 256, step):
			_r = '{0:03d}'.format(r)
			_g = '{0:03d}'.format(g)
			_b = '{0:03d}'.format(b)
			dict_key = '{}{}{}'.format(_r, _g, _b)
			all_rgb[dict_key] = [r, g, b]



'''
creating rgb_to_emojis

rgb_to_emojis = {
'000000000':["w_tiger-face_1f42f.png","w_tiger-face_1f42f.png", ...],
...
'255255255:["_white.png", "_white.png", ...]
}
'''

# pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open('../../data/twemoji/1x1_rgb.pickle', 'rb') as f:
	emoji_1x1_rgb = pickle.load(f)


top_num = 10  # THIS IS NOT STEP

# making 4 dicts for speed comparison
rgb_to_top_emojis = {}
rgb_to_all_emojis = {}


for rgb_key, rgb_array in all_rgb.items():
	print('calc for {}'.format(rgb_key))

	rgb_emojis = []
	rgb_ndarray = np.array(rgb_array)

	emoji_distance_dict = {}
	for emoji_name, emoji_rgb in emoji_1x1_rgb.items():
		nd_emoji_rgb = np.array(emoji_rgb)

		distance = (nd_emoji_rgb[0][0][0] - rgb_ndarray[0]) ** 2 \
				   + (nd_emoji_rgb[0][0][1] - rgb_ndarray[1]) ** 2 \
				   + (nd_emoji_rgb[0][0][2] - rgb_ndarray[2]) ** 2
		emoji_distance_dict[emoji_name] = distance



	"""
	>> [i for i in sorted(d.items(), key=itemgetter(1))]
	returns:[('emo2', 3), ('emo1', 5), ('emo3', 7)]

	>> [i[0] for i in sorted(d.items(), key=itemgetter(1))]
	returns:['emo2', 'emo1', 'emo3']
	"""
	top_emojis = [i[0] for i
					  in sorted(emoji_distance_dict.items(), key=itemgetter(1))[:top_num]
					  ]

	all_emojis = [i[0] for i
					  in sorted(emoji_distance_dict.items(), key=itemgetter(1))
					  ]

	rgb_to_top_emojis[rgb_key] = top_emojis
	rgb_to_all_emojis[rgb_key] = all_emojis


with open('../../data/twemoji/hash/alpha/step{}_type_top{}_emojis.pickle'.format(step, top_num), 'wb') as f:
	pickle.dump(rgb_to_top_emojis, f)

with open('../../data/twemoji/hash/alpha/step{}_type_all_emojis.pickle'.format(step), 'wb') as f:
	pickle.dump(rgb_to_all_emojis, f)

