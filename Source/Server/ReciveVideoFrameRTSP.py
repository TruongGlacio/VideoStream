import cv2
import os
from multiprocessing import Process
from datetime import datetime
import time
import os
import signal
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
class ReciveVideoFrameRTSP:
    def __init__(self):        
        self.video_folder_path_output = 'Output'
        if not os.path.exists(self.video_folder_path_output):
            os.mkdir(self.video_folder_path_output)

    def PlayVideoFromRTSP(self, play_status,rtsp_link):
        cv2_1 = cv2
        self.capture = cv2_1.VideoCapture(rtsp_link, cv2_1.CAP_FFMPEG)
        while play_status:
            result, frame = self.capture.read()
            if frame is None:
                print('Frame is Empty')
                return None
            cv2_1.imshow('video', frame)
            if cv2_1.waitKey(16) == ord("q"):
                play_status = False
        self.capture.release()
    
    def SaveStreamRTSPToVideo(self, timeout_seconds,fps,rtsp_link):
        print('SaveStreamRTSPToVideo function')
        cv2_1 = cv2
        self.capture = cv2_1.VideoCapture(rtsp_link, cv2_1.CAP_FFMPEG)
        video_file_name_follow_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        video_file_name_follow_time = video_file_name_follow_time.replace('-','_').replace(':','_').replace(' ','')
        video_path = os.path.join(self.video_folder_path_output, video_file_name_follow_time)+ '.avi'
        print(video_path)
        frame_width = int(self.capture.get(3))
        frame_height = int(self.capture.get(4))
        self.video_out = cv2_1.VideoWriter(video_path,cv2_1.VideoWriter_fourcc('M','J','P','G'), fps, (frame_width,frame_height))
        start = time.time()

        while True:
            done = time.time()
            result, frame = self.capture.read()
            if frame is None:
                print('Frame is Empty')
                cv2_1.waitKey(6)
                break
            cv2_1.imshow('video'+ rtsp_link, frame)
            self.video_out.write(frame)
            elapsed = done - start
            cv2_1.waitKey(6)
            if elapsed > timeout_seconds:
                break
        self.capture.release()
        self.video_out .release()


class QThreadForStreamVideo(QRunnable):
    def __init__(self, args_list):
        super(QThreadForStreamVideo, self).__init__()
        self.args_list = args_list
        print('Qthread init')
        self.reciveVideoFrameRTSP = ReciveVideoFrameRTSP()
    def run(self):
        # for i in range(10):
        #     print(i)
        #     time.sleep(1)
        print('Run qthread')
        time_out, fps, link = self.args_list
        print(time_out, fps, link)
        self.reciveVideoFrameRTSP.SaveStreamRTSPToVideo(time_out, fps, link)
        #self.reciveVideoFrameRTSP.PlayVideoFromRTSP(True,link)

if __name__ == '__main__':
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
    camlink1 = "rtsp://192.168.1.8:554"#
    camlink2 = "rtsp://192.168.1.4:554" 
    args_list1=(60,30,camlink1)
    args_list2=(60,15,camlink2)
    reciveVideoFrameRTSP = ReciveVideoFrameRTSP()
    reciveVideoFrameRTSP1 = ReciveVideoFrameRTSP()
    reciveVideoFrameRTSP2 = ReciveVideoFrameRTSP()
    # qThreadForStreamVideo1 = QThreadForStreamVideo(args_list = args_list1)
    # qThreadForStreamVideo1.setAutoDelete(True)
    # #QThreadPool.globalInstance().start(qThreadForStreamVideo1)
    # threadpool1 = QThreadPool()
    # threadpool1.start(qThreadForStreamVideo1)


    # qThreadForStreamVideo2 = QThreadForStreamVideo(args_list = args_list2)
    # qThreadForStreamVideo2.setAutoDelete(True)
    # #QThreadPool.globalInstance().start(qThreadForStreamVideo2)
    # threadpool2 = QThreadPool()
    # threadpool2.start(qThreadForStreamVideo2)

    p1 = Process(target=reciveVideoFrameRTSP.SaveStreamRTSPToVideo,args=args_list1)
    p2 = Process(target=reciveVideoFrameRTSP1.SaveStreamRTSPToVideo,args=args_list2)
    #p3 = Process(target=reciveVideoFrameRTSP2.SaveStreamRTSPToVideo,args=args_list1)
    p1.start()
    p2.start()
    #p3.start()
    p1.join()
    p2.join()
    #p3.join()