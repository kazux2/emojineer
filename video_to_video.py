
import cv2
from emojineer_video import emojineer
import numpy as np
from os import listdir
from os.path import isfile, join, splitext

def emojinize_video(target_video_path, save_path, conv):

    cap = cv2.VideoCapture(target_video_path)
    total_frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    ret, frame = cap.read()
    conv = conv
    frame = emojineer(frame, conv)
    converted_height = len(frame)
    converted_width = len(frame[0])

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # SEE: https://gist.github.com/takuma7/44f9ecb028ff00e2132e
    out = cv2.VideoWriter(save_path, fourcc, 29.97, (converted_width, converted_height))  # 毎回手動で変えなきゃいけない


    images = []
    counter = 0

    # while counter < 50:
    while(cap.isOpened()):
        print("processing: {} / {}".format(counter, total_frame_num))
        counter += 1
        ret, frame = cap.read()

        # duration = 15
        # start_conv = 0.07
        # end_conv = 0.01
        # conv_range = start_conv - end_conv
        # conv_diff = conv_range / duration
        #
        # conv = start_conv - conv_diff*(counter%duration)
        # conv = end_conv + conv_diff*(counter%duration)

        if ret:
            frame = emojineer(frame, conv)
            # print(len(frame), len(frame[0]), len(frame[0][0]))  # 動画を変えたら確認
            # cv2.imshow('frame',frame)
            out.write(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break



    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()




if __name__ == "__main__":
    file_name_base = "010ship.mp4"
    target_directory = "/Users/kazukiozone/privateKaihatsu/emoji/emojineer/target_video/2018summer_art_project/kai_premiere/cropped/"
    target_file_path = join(target_directory, file_name_base)
    print("processing for: ", file_name_base)
    save_directory = "/Users/kazukiozone/privateKaihatsu/emoji/emojineer/target_video/2018summer_art_project/kai_premiere/cropped_converted_highrez/"
    save_file_path = join(save_directory, file_name_base)
    # print(target_file_path, isfile(target_file_path))
    conv = 0.05
    print("conv:", conv)
    emojinize_video(target_file_path, save_file_path, conv)

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


