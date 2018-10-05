
import cv2
from emojineer_video import emojineer
import numpy as np
from os import listdir
from os.path import isfile, join, splitext
import math



file_name_base = "002plazma_zoom_out_02_conv001to005.mp4"
target_directory = "/Users/kazukiozone/privateKaihatsu/emoji/emojineer/target_video/2018summer_art_project/kai_premiere/cropped/"
target_file_path = join(target_directory, file_name_base)

save_directory = "/Users/kazukiozone/privateKaihatsu/emoji/emojineer/target_video/2018summer_art_project/kai_premiere/cropped_converted_highrez/"
save_file_path = join(save_directory, file_name_base)


cap = cv2.VideoCapture(target_file_path)
total_frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# ret, frame = cap.read()
# conv = conv
# frame = emojineer(frame, conv)
# converted_height = len(frame)
# converted_width = len(frame[0])

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # SEE: https://gist.github.com/takuma7/44f9ecb028ff00e2132e
# out = cv2.VideoWriter(save_file_path, fourcc, 29.97, (converted_width, converted_height))  # 毎回手動で変えなきゃいけない
out = cv2.VideoWriter(save_file_path, fourcc, 29.97, (1920, 1080))


images = []
counter = 0

background = np.zeros((1080,1920,3))


duration = total_frame_num
max_conv = 0.05  #最も荒い
min_conv = 0.01  #細かい
conv_range = max_conv - min_conv
conv_diff = conv_range / duration

# current_conv = max_conv
current_conv = min_conv

# while counter < 50:
while(cap.isOpened()):
    print("processing: {} / {}".format(counter, total_frame_num))
    counter += 1
    ret, frame = cap.read()

    # current_conv -= conv_diff  # conv 下がる　解像度　上がる
    current_conv += conv_diff  # 荒くする
    print("current_conv:", current_conv)
    if ret:
        frame = emojineer(frame, current_conv)

        print(frame.shape)
        print(background.shape)

        if frame.shape[0]<=1080:
            padding = math.floor((1080 - frame.shape[0])/2)
            background[padding:padding + frame.shape[0], :, :] = frame
        else:

            removable = math.floor((frame.shape[0] - 1080)/2)
            print(removable)
            background = frame[removable:removable + 1080, :, :]

        out.write(np.uint8(background))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break



# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()





# print(target_file_path, isfile(target_file_path))
# conv = 0.01
# emojinize_video(target_file_path, save_file_path, conv)

# target_directory = "/Users/kazukiozone/privateKaihatsu/emoji/emojineer/target_video/2018summer_art_project/kai_premiere/cropped"
# save_directory = "/Users/kazukiozone/privateKaihatsu/emoji/emojineer/target_video/2018summer_art_project/kai_premiere/cropped_converted"
#
#
# file_names = [f for f in listdir(target_directory) if isfile(join(target_directory, f))]
#
# conv = 0.008
#
# for file_name in file_names:
#     print("=== emojinize_video for {} ===".format(file_name))
#     root, ext = splitext(file_name)
#     if not ext in ['.mp4']:
#         continue
#
#     target_video_path = join(target_directory, file_name)
#     save_file_name = "{}_emoji_conv{}.mp4".format(file_name, conv)
#     save_path = join(save_directory, save_file_name)
#
#     emojinize_video(target_video_path, save_path, conv)


