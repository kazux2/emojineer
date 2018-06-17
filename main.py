from emojineer import Emojineer
import cv2

def main(target_file_name, conversion, similarities, converted_img_save_dir):
	print('====main() for {}'.format(target_file_name))
	# target_file_name = 'hokusai.jpg'
	target_file_name = target_file_name
	# conversion = 0.01 #0 ~ 1
	# similarity = 2600 #0~2614
	emojineer = Emojineer(target_file_name, conversion, similarities)
	cut_target_img = emojineer.split_target_image()

	# nearest_emoji_name_list1, nearest_emoji_name_list2, nearest_emoji_name_list3 = emojineer.find_nearest_emojis(cut_target_img)
	nearest_emoji_name_lists = emojineer.find_nearest_emojis(cut_target_img)
	print(nearest_emoji_name_lists)
	for emoji_name, list in nearest_emoji_name_lists.items():
		for obj in list:
			for sim, nearest_emoji_name_list in obj.items():
				print(sim)
				emojineer.concatinate_emojis(nearest_emoji_name_list, sim, converted_img_save_dir)

	# for nearest_emoji_name_list in nearest_emoji_name_lists:
	# 	print(len(nearest_emoji_name_lists))
	# 	emojineer.concatinate_emojis(nearest_emoji_name_list, 0, converted_img_save_dir)

	# converted_img = emojineer.concatinate_emojis(nearest_emoji_name_list1, 0, converted_img_save_dir)
	# converted_img = emojineer.concatinate_emojis(nearest_emoji_name_list2, 10, converted_img_save_dir)
	# converted_img = emojineer.concatinate_emojis(nearest_emoji_name_list3, 20, converted_img_save_dir)

	print('saved')
	# cv2.imshow('hokusai', converted_img)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()




if __name__ == '__main__':
	# conversion = 0.01 #0 ~ 1
	# conversions = [0.2, 0.1, 0.05, 0.025, 0.02]
	conversions = [0.2]

	# similarity = 2600 #0~2614
	# similarities = [0, 50, 2000, 2550]
	similarities = [0, 1, 2]
	# similarities = [0]

	# target_file_name = 'hokusai.jpg'
	# converted_img_save_dir = 'emojineer/converted_img_0603'
	# for conversion in conversions:
	# 	for similarity in similarities: # could be range(0,2594,500)
	# 		print("====similarity {}====".format(similarity))
	# 		main(target_file_name, conversion, similarity, converted_img_save_dir)

	# cv2.imshow('converted_img', converted_img)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()




	# target_file_name = 'zenigame.jpg'
	# converted_img_save_dir = 'emojineer/converted_img_0603'
	# for conversion in conversions:
	# 	for similarity in similarities:  # could be range(0,2594,500)
	# 		print("====similarity {}====".format(similarity))
	# 		main(target_file_name, conversion, similarity, converted_img_save_dir)


	target_file_name = '7-eleven_logo.png'
	converted_img_save_dir = 'emojineer/converted_img_0616'
	for conversion in conversions:
		main(target_file_name, conversion, similarities, converted_img_save_dir)


'''
	target_file_name = 'cry_emoji.jpg'
	converted_img_save_dir = 'emojineer/converted_img_0603'
	for conversion in conversions:
		for similarity in similarities:  # could be range(0,2594,500)
			print("====similarity {}====".format(similarity))
			main(target_file_name, conversion, similarity, converted_img_save_dir)



	target_file_name = 'funassi.jpg'
	converted_img_save_dir = 'emojineer/converted_img_0603'
	for conversion in conversions:
		for similarity in similarities:  # could be range(0,2594,500)
			print("====similarity {}====".format(similarity))
			main(target_file_name, conversion, similarity, converted_img_save_dir)



	target_file_name = 'pikachuu.jpg'
	converted_img_save_dir = 'emojineer/converted_img_0603'
	for conversion in conversions:
		for similarity in similarities:  # could be range(0,2594,500)
			print("====similarity {}====".format(similarity))
			main(target_file_name, conversion, similarity, converted_img_save_dir)



	target_file_name = 'super_mario_bros.png'
	converted_img_save_dir = 'emojineer/converted_img_0603'
	for conversion in conversions:
		for similarity in similarities:  # could be range(0,2594,500)
			print("====similarity {}====".format(similarity))
			main(target_file_name, conversion, similarity, converted_img_save_dir)




	target_file_name = 'zelda_glass.jpeg'
	converted_img_save_dir = 'emojineer/converted_img_0603'
	for conversion in conversions:
		for similarity in similarities:  # could be range(0,2594,500)
			print("====similarity {}====".format(similarity))
			main(target_file_name, conversion, similarity, converted_img_save_dir)




	target_file_name = 'gogh.jpg'
	converted_img_save_dir = 'emojineer/converted_img_0603'
	for conversion in conversions:
		for similarity in similarities:  # could be range(0,2594,500)
			print("====similarity {}====".format(similarity))
			main(target_file_name, conversion, similarity, converted_img_save_dir)



	target_file_name = 'mike_monster.jpeg'
	converted_img_save_dir = 'emojineer/converted_img_0603'
	for conversion in conversions:
		for similarity in similarities:  # could be range(0,2594,500)
			print("====similarity {}====".format(similarity))
			main(target_file_name, conversion, similarity, converted_img_save_dir)





	target_file_name = 'monet_sonnenschirm.jpg'
	converted_img_save_dir = 'emojineer/converted_img_0603'
	for conversion in conversions:
		for similarity in similarities:  # could be range(0,2594,500)
			print("====similarity {}====".format(similarity))
			main(target_file_name, conversion, similarity, converted_img_save_dir)




	target_file_name = 'lawson.jpg'
	converted_img_save_dir = 'emojineer/converted_img_0603'
	for conversion in conversions:
		for similarity in similarities:  # could be range(0,2594,500)
			print("====similarity {}====".format(similarity))
			main(target_file_name, conversion, similarity, converted_img_save_dir)





	target_file_name = 'picaso.jpg'
	converted_img_save_dir = 'emojineer/converted_img_0603'
	for conversion in conversions:
		for similarity in similarities:  # could be range(0,2594,500)
			print("====similarity {}====".format(similarity))
			main(target_file_name, conversion, similarity, converted_img_save_dir)






	target_file_name = 'zelda.jpg'
	converted_img_save_dir = 'emojineer/converted_img_0603'
	for conversion in conversions:
		for similarity in similarities:  # could be range(0,2594,500)
			print("====similarity {}====".format(similarity))
			main(target_file_name, conversion, similarity, converted_img_save_dir)




	target_file_name = 'familymart.png'
	converted_img_save_dir = 'emojineer/converted_img_0603'
	for conversion in conversions:
		for similarity in similarities:  # could be range(0,2594,500)
			print("====similarity {}====".format(similarity))
			main(target_file_name, conversion, similarity, converted_img_save_dir)


'''