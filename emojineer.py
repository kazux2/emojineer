import cv2

dir_path = 'emojineer/target_img'
target_file_name = '7-eleven_logo.png'

target_img = cv2.imread('{}/{}'.format(dir_path, target_file_name))
print(target_img.shape)
height, width = target_img.shape[:2]

convert_density = 50

h_number = height // convert_density
w_number = width // convert_density


cut_target_img = []
for h in range(h_number):
	horizon_cut = []
	for w in range(w_number):
		cut_piece = target_img[h:(h+1)*convert_density, w:(w+1)*convert_density]
		horizon_cut.append(cut_piece)
	cut_target_img.append(horizon_cut)

# cv2.imshow('name', cut_target_img[10][10])
# cv2.waitKey(0)
# cv2.destroyAllWindows()