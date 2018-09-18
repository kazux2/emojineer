
import cv2
from PIL import Image

from emojineer_video import emojineer


cap = cv2.VideoCapture('../target_video/tower-to-earth.mp4')

images = []


# counter = 0
# while counter < 50:
    # counter += 1

while cap.isOpened():

    ret, frame = cap.read()

    frame = emojineer(frame, 0.02)
    cv2.imshow('frame',frame)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    PIL_data = Image.fromarray(frame_rgb)  # convert cv2 -> PIL

    images.append(PIL_data)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


images[0].save('target_video/tower-to-earth_e01_e07.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=3, loop=0)


# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()
