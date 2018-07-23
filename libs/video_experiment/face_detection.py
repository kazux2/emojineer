import cv2
import time


face_cascade = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")

emoji = cv2.imread("data/whiten_emoji_apple/w_flushed-face_1f633.png")
e_w, e_h = emoji.shape[:2]
video =cv2.VideoCapture(0)

while True:
	check, frame = video.read()

	gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray,
										  scaleFactor=1.1,
										  minNeighbors=5)

	if len(faces) == 0:
		print("face not detected")
		continue

	print("{} faces detected".format(len(faces)))

	for x, y, w, h in faces:

		x_w = x + w
		y_h = y + h
		resized_emoji = cv2.resize(emoji, (w, h))
		re_w, re_h = resized_emoji.shape[:2]
		if re_w != w and re_h != h:
			continue
		try:
			frame[y:y_h, x:x_w] = resized_emoji
		except Exception as e:
			print("skipping:{}".format(e))
			print(w, h)
			print(re_w, re_h)

		cv2.imshow("Capturing", frame)

	key = cv2.waitKey(30)

	if key == ord('q'):
		break

video.release()
cv2.destroyAllWindows()