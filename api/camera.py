import cv2
import requests
import base64
import json
import time

font = cv2.FONT_HERSHEY_SIMPLEX
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        

    def __del__(self):
        self.video.release()

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        _, fr = self.video.read()
        #time.sleep(500)
       
        _, jpeg1 = cv2.imencode('.jpg', fr)
        files={"file":jpeg1}
        try:
            url="http://127.0.0.1:7000/api/predict"
            res = requests.post(url, files=files)
        except Exception as e:
            print(str(e))
        faces = json.loads(res.content)
        for face in faces:
            x, y, w, h = face['box'].values()

            cv2.putText(fr, face['emotion']+' '+face['probability'][:4],
                        (x, y-10), font, 0.75, (0, 0, 255), 2)
            cv2.rectangle(fr, (x, y), (x+w, y+h), (0, 0, 255), 2)
        #img = image_resize(img, width=600)
        _, jpeg = cv2.imencode('.jpg', fr)
        img = base64.encodebytes(jpeg.tobytes())
        context = {'image': img.decode('utf-8'), 'json': faces,'total':len(faces)}
        
        return jpeg.tobytes()