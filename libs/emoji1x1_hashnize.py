import json
import time
import os, sys
import numpy as np
from operator import itemgetter
from libs.rgbvalue_reduce_machine import RGBvalueReduceMachine

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

reducer = RGBvalueReduceMachine(5)

for emoji_name, emoji_rgb in whiten_emoji_1x1_rgb.items():

	print(emoji_rgb[0][0])
	print(reducer.rgb_value_reducer(emoji_rgb[0][0]))
