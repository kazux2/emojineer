import cv2
import numpy as np
from slic_class import slic


file_name_base = "test11"
cap = cv2.VideoCapture('{}.mp4'.format(file_name_base))

ret, frame = cap.read()
#conv = 0.2
#frame.astype(np.float64)
#frame = np.array(frame)
cv2.imwrite('temp.jpg', frame)
frame = slic(target_img='temp.jpg', n_segments=5000, compactness=50, sparseness=0.3, hash=0) #emojineerの場合、入力と出力で解像度が異なり、出力の解像度が動画作成に事前(17行目VideoWriter)に必要なため1フレームをここで取って調べてる
converted_height = len(frame)
converted_width = len(frame[0])

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # SEE: https://gist.github.com/takuma7/44f9ecb028ff00e2132e
out = cv2.VideoWriter('{}_e.mp4'.format(file_name_base), fourcc, 15.0, (converted_width, converted_height))  # 毎回手動で変えなきゃいけない

images = []
counter = 0

# while counter < 50:
while(cap.isOpened()):

    counter += 1
    ret, frame = cap.read()

    if ret:
        cv2.imwrite('temp.jpg', frame)
        frame = slic(target_img='temp.jpg', n_segments=5000, compactness=50, sparseness=0.3, hash=0)
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