import cv2
import json
import os
from os import listdir
from os.path import isfile, join
import numpy as np
from operator import itemgetter


class Emojineer():

	def __init__(self, target_file_name, conversion):
		self.dir_path = 'emojineer/target_img'
		self.target_file_name = target_file_name
		self.target_name, self.target_ext = os.path.splitext(target_file_name)

		self.target_img = cv2.imread('{}/{}'.format(self.dir_path, self.target_file_name))
		self.height, self.width = self.target_img.shape[:2]

		if conversion == 0:
			conversion = 0.01
		self.convolution_resolution = round(min([self.height,self.width]) * conversion)
		self.raws = self.height // self.convolution_resolution
		self.column = self.width // self.convolution_resolution

		self.whiten_emoji_path = 'data/whiten_emoji_apple'
		self.whiten_emoji_file_names = [f for f in listdir(self.whiten_emoji_path) if isfile(join(self.whiten_emoji_path, f))]
		with open('data/whiten_emoji_1x1_rgb.json', 'r') as f:
			self.whiten_emoji_1x1_rgb = json.load(f)



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
				cut_piece_1x1 = cv2.resize(cut_piece, (1,1))
				horizon_cut.append(cut_piece_1x1)

			cut_target_img.append(horizon_cut)

		return cut_target_img



	def find_nearest_emojis(self, cut_target_img):
		'''
		calc nearest emojis
		'''

		nearest_emoji_name_list = []

		for h in range(self.raws):
			horizon_emoji = []
			print('finding_nearest_emoji... {}/{}'.format(h+1, self.raws))
			for w in range(self.column):
				dist_candidate = {}

				for w_emoji_name in self.whiten_emoji_file_names:

					if not w_emoji_name == '.DS_Store':
						emoji_rgb = np.array(self.whiten_emoji_1x1_rgb[w_emoji_name])
						cut_piece_rgb = cut_target_img[h][w]
						distance = (emoji_rgb[0][0][0]-cut_piece_rgb[0][0][0])**2\
								   + (emoji_rgb[0][0][1]-cut_piece_rgb[0][0][1])**2\
								   + (emoji_rgb[0][0][2]-cut_piece_rgb[0][0][2])**2

						dist_candidate[w_emoji_name] = distance

				horizon_emoji.append(min(dist_candidate.items(), key=itemgetter(1))[0])
			nearest_emoji_name_list.append(horizon_emoji)

		with open('emojineer/calc_result/{}_nearest_emoji_names'.format(self.target_name), 'w') as f:
			json.dump(nearest_emoji_name_list, f, indent=2)

		return nearest_emoji_name_list


	def concatinate_emojis(self, nearest_emoji_name_list):
		'''
		concatinate emojis
		'''

		vertical_imgs = []
		print(nearest_emoji_name_list)
		print(self.raws, self.column)
		print(len(nearest_emoji_name_list))
		for h in range(self.raws):
			horison_imgs = []

			for w in range(self.column):
				print('concatinating emojis... {}-{}'.format(h, w))
				print('{}/{}'.format(self.whiten_emoji_path,
												nearest_emoji_name_list[h][w]))
				img = cv2.imread('{}/{}'.format(self.whiten_emoji_path,
												nearest_emoji_name_list[h][w]))
				horison_imgs.append(img)

			im_v = cv2.hconcat(horison_imgs)

			vertical_imgs.append(im_v)

		converted_img = cv2.vconcat(vertical_imgs)
		cv2.imshow('kakaka', converted_img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		cv2.imwrite('emojineer/converted_img/{}_conv_{}{}'.format(self.target_name, self.convolution_resolution, self.target_ext),
					converted_img)

		return converted_img






if __name__ == '__main__':
	target_file_name = '7-eleven_logo.png'

	emojineer = Emojineer(target_file_name, 0.2)
	cut_target_img = emojineer.split_target_image()

	nearest_emoji_name_list = emojineer.find_nearest_emojis(cut_target_img)
	converted_img = emojineer.concatinate_emojis(nearest_emoji_name_list)

	cv2.imshow('converted_img', converted_img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()















