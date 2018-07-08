from emojineer import Emojineer
from os import listdir
from os.path import isfile, join

def main(target_file_name, conversion, save_dir):

	emojineer = Emojineer(target_file_name=target_file_name,
						  conversion=conversion,
						  similarities=[0],
						  hash_step=5,
						  pickled_hash='data/pickle_w1x1_hash_dicts_0_256_5')


	loaded_img = emojineer.load_target_img('emojineer/target_img', target_file_name)

	cut_target_img = emojineer.split_target_image(loaded_img)

	nearest_emoji_name_lists_hash = emojineer.find_nearest_emojis_with_pickled_hash(cut_target_img, target_file_name)

	for emoji_name, list in nearest_emoji_name_lists_hash.items():
		for obj in list:
			for sim, nearest_emoji_name_list in obj.items():
				converted_img_hash = emojineer.concatinate_emojis(nearest_emoji_name_list,
																  similarity=sim,
																  save_dir=save_dir,
																  target_file_name=target_file_name)

	print('saved')


if __name__ == '__main__':

	conversions = [0.3, 0.2, 0.1, 0.08, 0.05, 0.03, 0.025, 0.02, 0.015, 0.01] # 0 ~ 1

	dir_path = 'emojineer/target_img'
	file_names = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
	save_dir = 'emojineer/converted_img_0705'

	for target_file_name in file_names:
		print("===========main for {}===========".format(target_file_name))

		for conversion in conversions:

			main(target_file_name, conversion, save_dir)
