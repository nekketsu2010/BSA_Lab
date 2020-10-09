import sys
import cv2 # OpenCV のインポート
import time
import pyautogui as pgui
'''
参考
@link http://ensekitt.hatenablog.com/entry/2017/12/19/200000
@link https://note.nkmk.me/python-opencv-face-detection-haar-cascade/
@link https://note.nkmk.me/python-opencv-mosaic/
@link http://workpiles.com/2015/04/opencv-detectmultiscale-scalefactor/
'''

# スペースキーを入力する関数
def spaceKey():
    pgui.typewrite(" ")

# VideoCaptureのインスタンスを作成する。
# 引数でカメラを選べれる。
cap = cv2.VideoCapture(0)

if cap.isOpened() is False:
    print("can not open camera")
    sys.exit()

# 評価器を読み込み
# https://github.com/opencv/opencv/tree/master/data/haarcascades
cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye_tree_eyeglasses.xml')

def mosaic(src, ratio=0.1):
    small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
    return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

def mosaic_area(src, x, y, width, height, ratio=0.1):
    dst = src.copy()
    dst[y:y + height, x:x + width] = mosaic(dst[y:y + height, x:x + width], ratio)
    return dst

def checkWink():
    # VideoCaptureから1フレーム読み込む
    ret, frame = cap.read()

    # そのままの大きさだと処理速度がきついのでリサイズ
    frame = cv2.resize(frame, (int(frame.shape[1]*0.7), int(frame.shape[0]*0.7)))

    # 処理速度を高めるために画像をグレースケールに変換したものを用意
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 顔検出
    facerect = cascade.detectMultiScale(
        gray,
        scaleFactor=1.11,
        minNeighbors=3,
        minSize=(100, 100)
    )

    if len(facerect) != 0:
        for x, y, w, h in facerect:
            # 顔の部分(この顔の部分に対して目の検出をかける)
            face_gray = gray[y: y + h, x: x + w]

            # くり抜いた顔の部分を表示(処理には必要ない。ただ見たいだけ。)
            show_face_gray = cv2.resize(face_gray, (int(gray.shape[1]), int(gray.shape[0])))
            cv2.imshow('face', show_face_gray)

            # 顔の部分から目の検出
            eyes = eye_cascade.detectMultiScale(
                face_gray,
                scaleFactor=1.11, # ここの値はPCのスペックに依存するので適宜修正してください
                minNeighbors=3,
                minSize=(15, 15)
            )

            if len(eyes) == 0:
                return True
    return False

count = 0
while True:
    for i in range(3):
        wink = checkWink()
        count += int(wink)
        time.sleep(0.05)
    
    if count == 3:
        # 目が閉じられたとみなす
        spaceKey() # スペースキー入力
        time.sleep(0.25)
        # cv2.putText(
        #     frame,
        #     'close your eyes',
        #     (x, y - 10), # 位置を少し調整
        #     cv2.FONT_HERSHEY_PLAIN,
        #     2,
        #     (0, 255,0),
        #     2,
        #     cv2.LINE_AA
        # )
        # # 顔検出した部分に枠を描画
        # cv2.rectangle(
        #     frame,
        #     (x, y),
        #     (x + w, y + h),
        #     (255, 255, 255),
        #     thickness=2
        # )

        # cv2.imshow('frame', frame)

    count = 0

    # キー入力を1ms待って、k が27（ESC）だったらBreakする
    k = cv2.waitKey(1)
    if k == 27:
        break

# キャプチャをリリースして、ウィンドウをすべて閉じる
cap.release()
cv2.destroyAllWindows()