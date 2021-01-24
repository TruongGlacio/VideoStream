import cv2
import os
from multiprocessing import Process
from datetime import datetime
import time

class ReciveVideoFrameRTSP:
    def __init__(self):
        super().__init__()
        
        self.video_folder_path_output = 'Output'
        if not os.path.exists(self.video_folder_path_output):
            os.mkdir(self.video_folder_path_output)

    def PlayVideoFromRTSP(self, play_status):

        while play_status:
            result, frame = self.capture.read()
            cv2_1 = cv2
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
            cv2_1.imshow('video', frame)
            self.video_out.write(frame)
            elapsed = done - start
            cv2_1.waitKey(6)
            if elapsed > timeout_seconds:
                break
        self.capture.release()
        self.video_out .release()

if __name__ == '__main__':
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
    reciveVideoFrameRTSP = ReciveVideoFrameRTSP()
    reciveVideoFrameRTSP1 = ReciveVideoFrameRTSP()
    camlink = "rtsp://192.168.1.15:554"#"rtsp://192.168.1.4:554" 
    #reciveVideoFrameRTSP.SetUpRtsp(camlink)
    args_list=(60,10,camlink)
    p1 = Process(target=reciveVideoFrameRTSP.SaveStreamRTSPToVideo,args=args_list)

    p2 = Process(target=reciveVideoFrameRTSP1.SaveStreamRTSPToVideo,args=args_list)
    p1.start()
    p1.join()
    p2.start()
    p2.join()