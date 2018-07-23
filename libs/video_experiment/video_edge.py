"""
https://qiita.com/hitomatagi/items/12a2eceaf65f142ec3df
"""

import cv2

# cv2.cv.CV_FOURCC
def cv_fourcc(c1, c2, c3, c4):
    return (ord(c1) & 255) + ((ord(c2) & 255) << 8) + \
        ((ord(c3) & 255) << 16) + ((ord(c4) & 255) << 24)


if __name__ == '__main__':
    # 定数定義
    ESC_KEY = 27     # Escキー
    INTERVAL= 33     # 待ち時間
    FRAME_RATE = 30  # fps

    ORG_WINDOW_NAME = "org"
    GAUSSIAN_WINDOW_NAME = "gaussian"

    GAUSSIAN_FILE_NAME = "gaussian.avi"

    DEVICE_ID = 0

    # カメラ映像取得
    cap = cv2.VideoCapture(DEVICE_ID)

    # 保存ビデオファイルの準備
    end_flag, c_frame = cap.read()
    height, width, channels = c_frame.shape
    rec = cv2.VideoWriter(GAUSSIAN_FILE_NAME, \
                          cv_fourcc('X', 'V', 'I', 'D'), \
                          FRAME_RATE, \
                          (width, height), \
                          True)

    # ウィンドウの準備
    cv2.namedWindow(ORG_WINDOW_NAME)
    cv2.namedWindow(GAUSSIAN_WINDOW_NAME)

    # 変換処理ループ
    while end_flag == True:
        # ガウシアン平滑化
        g_frame = cv2.GaussianBlur(c_frame, (15, 15), 10)

        # フレーム表示
        cv2.imshow(ORG_WINDOW_NAME, c_frame)
        cv2.imshow(GAUSSIAN_WINDOW_NAME, g_frame)

        # フレーム書き込み
        rec.write(g_frame)

        # Escキーで終了
        key = cv2.waitKey(INTERVAL)
        if key == ESC_KEY:
            break

        # 次のフレーム読み込み
        end_flag, c_frame = cap.read()

    # 終了処理
    cv2.destroyAllWindows()
    cap.release()
    rec.release()