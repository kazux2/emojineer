
import cv2
from emojineer_video import emojineer


file_name_base = "penice"
cap = cv2.VideoCapture('/Users/kazukiozone/privateKaihatsu/emoji/emojineer/target_video/{}.mp4'.format(file_name_base))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # SEE: https://gist.github.com/takuma7/44f9ecb028ff00e2132e
out = cv2.VideoWriter('{}_e.mp4'.format(file_name_base), fourcc, 15.0, (1080, 600))  # 毎回手動で変えなきゃいけない


images = []
counter = 0

# while counter < 50:
while(cap.isOpened()):

    counter += 1
    ret, frame = cap.read()
    conv = 0.02
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
        cv2.imshow('frame',frame)
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break


# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
