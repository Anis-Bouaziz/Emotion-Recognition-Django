
import threading
import cv2
import numpy as np



class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
        
    def __del__(self):
        self.video.release()
    
    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
    
    def get_frame(self):
        return self.frame   






