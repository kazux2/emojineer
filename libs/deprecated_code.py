
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
		print('finding_nearest_emoji... {}/{}'.format( h +1, self.raws))
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
				distance = (emoji_rgb[0][0][0 ] -cut_piece_rgb[0][0][0] )* *2 \
						   + (emoji_rgb[0][0][1 ] -cut_piece_rgb[0][0][1] )* *2 \
						   + (emoji_rgb[0][0][2 ] -cut_piece_rgb[0][0][2] )* *2

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

	return {self.target_file_name :[nearest_emoji_name_lists]}
	# return nearest_emoji_name_list1, nearest_emoji_name_list2, nearest_emoji_name_list3


def find_nearest_emojis_with_hash(self, cut_target_img):
	'''
	calc nearest emojis
	'''
	with open('data/num_wemoji_dict.json', 'r') as f:
		num_wemoji_dict = json.load(f)
	nearest_emoji_name_lists = {}
	for similarity in self.similarities:
		nearest_emoji_name_lists[similarity] = []

	for h in range(self.raws):
		horizon_emojis = {}
		for similarity in self.similarities:
			horizon_emojis[similarity] = []

		print('finding_nearest_emoji... {}/{}'.format( h +1, self.raws))
		for w in range(self.column):

			cut_piece_rgb = cut_target_img[h][w]

			reducer = RGBvalueReduceMachine(self.hash_step) # hashの解像度と揃える
			cut_piece_rgb_list = reducer.rgb_value_reducer(cut_piece_rgb[0][0].tolist())

			_r = '{0:03d}'.format(cut_piece_rgb_list[0])
			_g = '{0:03d}'.format(cut_piece_rgb_list[1])
			_b = '{0:03d}'.format(cut_piece_rgb_list[2])

			dict_key = '{}{}{}'.format(_r, _g, _b)

			with open('{}/{}.json'.format(self.hash_dict_path ,dict_key), 'r') as f:
				w1x1_hash = json.load(f)

			# from libs.db_access import W1x1RGBtoEmojiname
			# print(dict_key)
			# query = W1x1RGBtoEmojiname.get_or_none(W1x1RGBtoEmojiname.rgb_value == dict_key)
			#
			# if query != None:
			# 	print("selected row:", query.emoji_file_name)

			for similarity in self.similarities:
				horizon_emojis[similarity].append(num_wemoji_dict[str(w1x1_hash[similarity])])
				# if query != None:
				# 	horizon_emojis[similarity].append(query.emoji_file_name)
				# else:
				# 	horizon_emojis[similarity].append("_white.png")

		for similarity, horizon_emoji in horizon_emojis.items():
			nearest_emoji_name_lists[similarity].append(horizon_emoji)

	return {self.target_file_name: [nearest_emoji_name_lists]}