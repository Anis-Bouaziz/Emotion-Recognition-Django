import os
import threading
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow as tf
from keras.models import load_model
from scipy import spatial

      

def draw_bbox_all(img, ann, img_height, img_width,emotion_classifier,mask):
    """draw bboxes and landmarks"""
    Masks = ["ON", "OFF"]
    EMOTIONS = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]#fer
    # bbox
    x1, y1, x2, y2 = int(ann[0] * img_width), int(ann[1] * img_height), \
                     int(ann[2] * img_width), int(ann[3] * img_height)
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    roi = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    roi = roi[y1:y2, x1:x2]
    roi = cv2.resize(roi, (48, 48))
    
    roi = roi.astype("float") / 255.0
    roi = img_to_array(roi)
    roi = np.expand_dims(roi, axis=0)
    preds = emotion_classifier.predict(roi)[0]
    emotion_probability = np.max(preds)
    label = EMOTIONS[preds.argmax()]

    #Mask
    roi2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    roi2 = roi2[y1:y2, x1:x2]
    roi2=cv2.resize(roi2,(224,224))
    roi2 = roi2.astype("float") / 255.0
    roi2 = img_to_array(roi2)
    roi2 = np.expand_dims(roi2, axis=0)
    preds2 = mask.predict(roi2)[0]
    mask_probability = np.max(preds)
    label2 = Masks[preds2.argmax()]
    if label2 == 'ON':
        color=(0,255,0)
    else:
        color=(0,0,255)
    # confidence
    text_emotion = label+" {:.2f}".format(emotion_probability)
    text_mask=label2+" {:.2f}".format(mask_probability)
    cv2.putText(img, text_emotion, (int(ann[0] * img_width), int(ann[1] * img_height)-20),
                 cv2.FONT_HERSHEY_DUPLEX, 0.5, (200, 0, 255))
    cv2.putText(img, text_mask, (int(ann[0] * img_width), int(ann[1] * img_height)),
                 cv2.FONT_HERSHEY_DUPLEX, 0.5, color)
    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)




os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'
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
        img_raw = self.frame
        #_,img_raw = cv2.imencode('.jpg',image)
        img_height_raw, img_width_raw,_ = img_raw.shape
        img = np.float32(img_raw.copy())
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # pad input image to avoid unmatched shape problem
        img, pad_params = pad_input_image(img, max_steps=max([8, 16, 32]))
    
        outputs = model(img[np.newaxis, ...]).numpy()
        
        # recover padding effect
        outputs = recover_pad_output(outputs, pad_params)
        json=[]
        for prior_index in range(len(outputs)):
            draw_bbox_all(img_raw, outputs[prior_index], img_height_raw,
                                    img_width_raw,emotion_classifier,mask)
        _,img = cv2.imencode('.jpg',img_raw)    
        return img.tobytes()