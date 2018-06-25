import cv2
import json
import os
from os import listdir
from os.path import isfile, join, splitext
import numpy as np
from operator import itemgetter


class Emojineer():

	def __init__(self, target_file_name, conversion, similarities):
		self.dir_path = 'emojineer/target_img'
		self.target_file_name = target_file_name
		self.target_name, self.target_ext = os.path.splitext(target_file_name)

		self.target_img = cv2.imread('{}/{}'.format(self.dir_path, self.target_file_name))
		self.height, self.width = self.target_img.shape[:2]

		if conversion == 0:
			conversion = 0.01

		self.conversion = conversion
		print("INFO:\t{{\"conversion\":{}}}".format(self.conversion))

		self.convolution_resolution = round(min([self.height,self.width]) * conversion)
		self.raws = self.height // self.convolution_resolution
		self.column = self.width // self.convolution_resolution

		self.similarities = similarities
		# self.similarity1 = 0
		# self.similarity2 = 0 + 10
		# self.similarity3 = 0 + 20

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
		nearest_emoji_name_lists = {}
		for similarity in self.similarities:
			nearest_emoji_name_lists[similarity] = []
		# nearest_emoji_name_list1 = []
		# nearest_emoji_name_list2 = []
		# nearest_emoji_name_list3 = []

		for h in range(self.raws):
			horizon_emojis = {}
			for similarity in self.similarities:
				horizon_emojis[similarity] = []
			# horizon_emoji1 = []
			# horizon_emoji2 = []
			# horizon_emoji3 = []
			print('finding_nearest_emoji... {}/{}'.format(h+1, self.raws))
			for w in range(self.column):
				dist_candidate = {}

				for w_emoji_name in self.whiten_emoji_file_names:

					root, ext = splitext(w_emoji_name)
					if not ext in ['.png', '.jpeg', '.jpg']:
						continue

					if w_emoji_name == '.DS_Store':
						continue

					emoji_rgb = np.array(self.whiten_emoji_1x1_rgb[w_emoji_name])
					cut_piece_rgb = cut_target_img[h][w]
					distance = (emoji_rgb[0][0][0]-cut_piece_rgb[0][0][0])**2\
							   + (emoji_rgb[0][0][1]-cut_piece_rgb[0][0][1])**2\
							   + (emoji_rgb[0][0][2]-cut_piece_rgb[0][0][2])**2

					dist_candidate[w_emoji_name] = distance

				# horizon_emoji.append(min(dist_candidate.items(), key=itemgetter(1))[0]) #the most similar
				# horizon_emoji1.append(sorted(dist_candidate.items(), key=itemgetter(1))[self.similarity1][0])
				# horizon_emoji2.append(sorted(dist_candidate.items(), key=itemgetter(1))[self.similarity2][0])
				# horizon_emoji3.append(sorted(dist_candidate.items(), key=itemgetter(1))[self.similarity3][0])

				for similarity in self.similarities:
					# horizon_emoji_temp = []
					# horizon_emoji_temp.append(sorted(dist_candidate.items(), key=itemgetter(1))[similarity][0])
					# horizon_emojis[similarity] = horizon_emoji_temp
					horizon_emojis[similarity].append(sorted(dist_candidate.items(), key=itemgetter(1))[similarity][0])

			# for similarity in self.similarities:
			# 	nearest_emoji_name_lists[similarity] = horizon_emojis[similarity]

			for similarity, horizon_emoji in horizon_emojis.items():
				nearest_emoji_name_lists[similarity].append(horizon_emoji)

			# nearest_emoji_name_list1.append(horizon_emoji1)
			# nearest_emoji_name_list2.append(horizon_emoji2)
			# nearest_emoji_name_list3.append(horizon_emoji3)

		return {self.target_file_name:[nearest_emoji_name_lists]}
		# return nearest_emoji_name_list1, nearest_emoji_name_list2, nearest_emoji_name_list3


	def concatinate_emojis(self, nearest_emoji_name_list, similarity, converted_img_save_dir):
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
		cv2.imwrite('{}/{}_s{}_c{}{}'.format(converted_img_save_dir, self.target_name, similarity, self.conversion, self.target_ext),
					converted_img)

		return converted_img


if __name__ == '__main__':
	target_file_name = '7-eleven_logo.png'
	converted_img_save_dir = 'emojineer/converted_img_0616'

	emojineer = Emojineer(target_file_name, conversion=0.2, similarities=[0])
	cut_target_img = emojineer.split_target_image()

	nearest_emoji_name_lists = emojineer.find_nearest_emojis(cut_target_img)
	for emoji_name, list in nearest_emoji_name_lists.items():
		for obj in list:
			for sim, nearest_emoji_name_list in obj.items():
				converted_img = emojineer.concatinate_emojis(nearest_emoji_name_list, sim, converted_img_save_dir)


	cv2.imshow('converted_img', converted_img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()















