import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.dirname(__file__))
import cv2
import json
import os
import time
import pickle
from os import listdir
from os.path import isfile, join, splitext
import numpy as np
from operator import itemgetter
from libs.rgbvalue_reduce_machine import RGBvalueReduceMachine

class Emojineer():

	def __init__(self, target_file_path, conversion, similarities, hash_step, pickled_hash):
		self.target_file_path = target_file_path
		self.target_img = cv2.imread(target_file_path) # メソッド切り出してそこに直接ファイル名渡したい
		self.height, self.width = self.target_img.shape[:2]

		if conversion == 0:
			conversion = 0.01

		self.conversion = conversion
		print("INFO:\t{{\"conversion\":{}}}".format(self.conversion))

		self.convolution_resolution = round(min([self.height,self.width]) * conversion)
		self.raws = self.height // self.convolution_resolution
		self.column = self.width // self.convolution_resolution

		self.similarities = similarities

		self.hash_step = hash_step

		with open(pickled_hash, 'rb') as f:
			self.hash_dict = pickle.load(f)

		cwd = os.path.dirname(__file__)
		self.whiten_emoji_path = os.path.join(cwd, 'data/whiten_emoji_apple')
		self.whiten_emoji_file_names = [f for f in listdir(self.whiten_emoji_path) if isfile(join(self.whiten_emoji_path, f))]

		with open(os.path.join(cwd,'data/whiten_emoji_1x1_rgb.json'), 'r') as f:
			self.whiten_emoji_1x1_rgb = json.load(f)


	# def load_target_img(self, dir_path, target_file_name):
	#
	# 	loaded_img = cv2.imread('{}/{}'.format(dir_path, target_file_name))
	#
	# 	return loaded_img


	def split_target_image(self) -> list:
		'''
		cut target img
		'''

		cut_target_img = []
		for h in range(self.raws):
			horizon_cut = []
			r = h * self.convolution_resolution
			r_ = (h + 1) * self.convolution_resolution

			for w in range(self.column):
				c = w * self.convolution_resolution
				c_ = (w + 1) * self.convolution_resolution
				cut_piece = self.target_img[r:r_, c:c_]
				cut_piece_1x1 = cv2.resize(cut_piece, (1,1)) #ToDo ここ大地くんの方法適用
				horizon_cut.append(cut_piece_1x1)

			cut_target_img.append(horizon_cut)

		return cut_target_img



	def find_nearest_emojis_with_pickled_hash(self, cut_target_img):
		'''
		calc nearest emojis
		'''
		cwd = os.path.dirname(__file__)
		with open(os.path.join(cwd, 'data/num_wemoji_dict.json'), 'r') as f:
			num_wemoji_dict = json.load(f)

		nearest_emoji_name_lists = {}
		for similarity in self.similarities:
			nearest_emoji_name_lists[similarity] = [] #FIXME defaultdictを使えばここを省略できる

		for h in range(self.raws):
			horizon_emojis = {}
			for similarity in self.similarities:
				horizon_emojis[similarity] = []

			print('finding_nearest_emoji... {}/{}'.format(h+1, self.raws))
			for w in range(self.column):

				cut_piece_rgb = cut_target_img[h][w]

				reducer = RGBvalueReduceMachine(self.hash_step) # hashの解像度と揃える
				cut_piece_rgb_list = reducer.rgb_value_reducer(cut_piece_rgb[0][0].tolist())

				_r = '{0:03d}'.format(cut_piece_rgb_list[0])
				_g = '{0:03d}'.format(cut_piece_rgb_list[1])
				_b = '{0:03d}'.format(cut_piece_rgb_list[2])

				dict_key = '{}{}{}'.format(_r, _g, _b)

				w1x1_hash = self.hash_dict[dict_key]

				for similarity in self.similarities:

					horizon_emojis[similarity].append(num_wemoji_dict[str(w1x1_hash[similarity])])

			for similarity, horizon_emoji in horizon_emojis.items():
				nearest_emoji_name_lists[similarity].append(horizon_emoji)

		target_file_name = self.target_file_path # pathからfilenameだけ切り取って使いたいかも

		return {target_file_name: [nearest_emoji_name_lists]}



	def concatinate_emojis_and_save_image(self, nearest_emoji_name_list, similarity, save_dir, target_file_name):
		'''
		concatinate emojis
		'''
		print(len(nearest_emoji_name_list), self.raws)
		print(len(nearest_emoji_name_list[0]), self.column)

		vertical_imgs = []

		for h in range(self.raws):
			horison_imgs = []

			for w in range(self.column):
				img = cv2.imread('{}/{}'.format(self.whiten_emoji_path,
												nearest_emoji_name_list[h][w]))
				horison_imgs.append(img)

			im_v = cv2.hconcat(horison_imgs)

			vertical_imgs.append(im_v)


		converted_img = cv2.vconcat(vertical_imgs)
		target_name, target_ext = os.path.splitext(target_file_name)

		x = self.convolution_resolution * self.column
		y = self.convolution_resolution * self.raws

		resized_converted_img = cv2.resize(converted_img, (1080,int(1080*y/x)))
		_conversion = "{0:04d}".format(int(self.conversion * 10000))
		cv2.imwrite('{}/{}_step_{}_sim_{}_c_{}{}'.format(save_dir, target_name, self.hash_step, similarity, _conversion, target_ext),
					resized_converted_img)

		# cv2.imshow('converted_img_hash', converted_img_hash)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()

		# return resized_converted_img



def emojineer(target_file_path, conversion, save_dir, save_name):

	cwd = os.path.dirname(__file__)
	emojineer = Emojineer(target_file_path=target_file_path,
						  conversion=conversion,
						  similarities=[0],
						  hash_step=5,
						  pickled_hash=os.path.join(cwd, 'data/pickle_w1x1_hash_dicts_0_256_5'))

	cut_target_img = emojineer.split_target_image()

	nearest_emoji_names = emojineer.find_nearest_emojis_with_pickled_hash(cut_target_img)

	# for emoji_name, list in nearest_emoji_names.items():
	for list in nearest_emoji_names.values():
		for obj in list:
			for sim, nearest_emoji_name_list in obj.items():
				emojineer.concatinate_emojis_and_save_image(nearest_emoji_name_list,
														  similarity=sim,
														  save_dir=save_dir,
														  target_file_name=save_name)

	print('saved')



if __name__ == '__main__':

	# conversions = [0.5, 0.1, 0.2, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.08, 0.075, 0.05, 0.04, 0.03, 0.025, 0.02, 0.017, 0.015, 0.013, 0.01] # 0 ~ 1
	conversions = [0.1]
	dir_path = 'target_img/hokusai'
	file_names = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
	save_dir = 'outputs'

	for target_file_name in file_names:
		if target_file_name == '.DS_Store':
			continue
		print("===========main for {}===========".format(target_file_name))

		for conversion in conversions:
			target_file_path = dir_path + "/" + target_file_name
			emojineer(target_file_path, conversion, save_dir, target_file_name)





