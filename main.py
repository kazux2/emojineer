from emojineer import Emojineer
import cv2

def main(target_file_name, conversion, similarities, converted_img_save_dir):
	print('=========main.py for {}========='.format(target_file_name))
	# target_file_name = 'hokusai.jpg'
	target_file_name = target_file_name
	emojineer = Emojineer(target_file_name, conversion, similarities)
	cut_target_img = emojineer.split_target_image()

	nearest_emoji_name_lists = emojineer.find_nearest_emojis(cut_target_img)
	for emoji_name, list in nearest_emoji_name_lists.items():
		for obj in list:
			for sim, nearest_emoji_name_list in obj.items():
				emojineer.concatinate_emojis(nearest_emoji_name_list, sim, converted_img_save_dir)

	print('saved')
	# cv2.imshow('hokusai', converted_img)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

if __name__ == '__main__':
	conversions = [0.2, 0.1, 0.08, 0.01] # 0 ~ 1

	similarities = [0, 10, 20, 500, 1000, 2000, 2500, 2600, 2610]

	converted_img_save_dir = 'emojineer/converted_img_0616'

	target_file_name = '7-eleven_logo.png'
	for conversion in conversions:
		main(target_file_name, conversion, similarities, converted_img_save_dir)

	# target_file_name = 'hokusai.jpg'
	# for conversion in conversions:
	# 	main(target_file_name, conversion, similarities, converted_img_save_dir)
	#
	# target_file_name = 'zenigame.jpg'
	# for conversion in conversions:
	# 	main(target_file_name, conversion, similarities, converted_img_save_dir)
	#
	# target_file_name = 'cry_emoji.jpg'
	# for conversion in conversions:
	# 	main(target_file_name, conversion, similarities, converted_img_save_dir)
	#
	# target_file_name = 'funassi.jpg'
	# for conversion in conversions:
	# 	main(target_file_name, conversion, similarities, converted_img_save_dir)
	#
	# target_file_name = 'pikachuu.jpg'
	# for conversion in conversions:
	# 	main(target_file_name, conversion, similarities, converted_img_save_dir)
	#
	# target_file_name = 'super_mario_bros.png'
	# for conversion in conversions:
	# 	main(target_file_name, conversion, similarities, converted_img_save_dir)
	#
	# target_file_name = 'zelda_glass.jpeg'
	# for conversion in conversions:
	# 	main(target_file_name, conversion, similarities, converted_img_save_dir)
	#
	# target_file_name = 'gogh.jpg'
	# for conversion in conversions:
	# 	main(target_file_name, conversion, similarities, converted_img_save_dir)
	#
	# target_file_name = 'mike_monster.jpeg'
	# for conversion in conversions:
	# 	main(target_file_name, conversion, similarities, converted_img_save_dir)
	#
	# target_file_name = 'monet_sonnenschirm.jpg'
	# for conversion in conversions:
	# 	main(target_file_name, conversion, similarities, converted_img_save_dir)
	#
	# target_file_name = 'lawson.jpg'
	# for conversion in conversions:
	# 	main(target_file_name, conversion, similarities, converted_img_save_dir)
	#
	# target_file_name = 'picaso.jpg'
	# for conversion in conversions:
	# 	main(target_file_name, conversion, similarities, converted_img_save_dir)
	#
	# target_file_name = 'zelda.jpg'
	# for conversion in conversions:
	# 	main(target_file_name, conversion, similarities, converted_img_save_dir)
	#
	# target_file_name = 'familymart.png'
	# for conversion in conversions:
	# 	main(target_file_name, conversion, similarities, converted_img_save_dir)
