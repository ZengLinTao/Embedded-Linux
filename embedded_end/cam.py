import cv2
import io
from picamera import PiCamera 
import numpy as np 
from threading import Thread
import base64
import mqtt_pub
import time
from threading import Thread 

class Camera(Thread):
    def __init__(self, thread_name):
        Thread.__init__(self, name=thread_name)
        self.__topic__ = 'monitor'
        self.__frame__ = None
        self.__frameList__ = list()
        self.__avg_frame = None
        self.__first_frame__ = None

    def run(self):
        with PiCamera() as camera:
            camera.resolution = (960, 480)
            camera.framerate = 10
            stream = io.BytesIO()

            bs = cv2.createBackgroundSubtractorKNN(detectShadows=True)
            bs.setHistory(20)

            frames = 0
            for f in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
                data = np.fromstring(stream.getvalue(), dtype=np.uint8)

                frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                fg_mask = bs.apply(gray)
                if frames < 20:
                    frames+=1
                    continue

                th = cv2.threshold(fg_mask.copy(), 244, 255, cv2.THRESH_BINARY)[1]
                th = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
                dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 3)), iterations=2)
                # 获取所有检测框
                image, contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for c in contours:
                    # 获取矩形框边界坐标
                    x, y, w, h = cv2.boundingRect(c)
                    # 计算矩形框的面积
                    area = cv2.contourArea(c)
                    if area > 500:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        self.__frame__ = frame
                        thread = Thread(target=self.pub_monitor)
                        thread.start()
                        # if detect
                stream.seek(0)
                cv2.imshow('dilated', dilated)
                cv2.imshow('frame', frame)
                key = cv2.waitKey(1) & 0xff
                if key == ord('q'):
                    break

        
    def pub_monitor(self):
        self.__frame__ = base64.b64encode(self.__frame__).decode('utf-8')
        json_str =  '{"topic":"%s","time":%f, "data":"%s"}' % (self.__topic__, time.time(), self.__frame__)
        mqtt_pub.pub_info(self.__topic__, json_str)
        print(self.__topic__)