
import sys
import time
import cv2
camera = None

# OpenCV의 VideoCapture 객체 초기화
def init(camera_id=0, width=640, height=480, buffer_size=1):
        global camera
        camera = cv2.VideoCapture(camera_id, cv2.CAP_V4L)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        camera.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)

# 사진을 촬영하고 이미지 데이터 리턴
def take_picture(most_recent=False):
        global camera
        # most_recent가 True이면 버퍼에 저장되어 있는 프레임을 전부 버리도록 한다.
        len = 0 if most_recent == False else camera.get(cv2.CAP_PROP_BUFFERSIZE)
        while(len > 0):
                camera.grab()   # 버퍼에 저장되어 있는 프레임을 버린다.
                len -= 1
        success, image = camera.read()
        if not success:
                return None

        return image

# 카메라 사용이 끝났을 때 VideoCapture 객체 해제
def final():
        if camera != None:
                camera.release()
        camera = None
