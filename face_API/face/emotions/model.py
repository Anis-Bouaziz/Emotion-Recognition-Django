
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from keras.models import load_model

class Xception(object):
    def __init__(self,retina):
        model_path="face_API/face/emotions/emotion.h5"
        self.model= load_model(model_path, compile=False)
        self.retina=retina
    def __del__(self):
        del self.model
        del self.retina
    def predict(self,face):
        EMOTIONS = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]#fer
        
        roi = cv2.resize(face, (48, 48))
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        preds = self.model.predict(roi)[0]
        emotion_probability = np.max(preds)
        label = EMOTIONS[preds.argmax()]
        return label,emotion_probability
    def draw(self,image):
        img_height, img_width, _ = image.shape
        faces=self.retina.predict(image)
        
        for face in faces:
            
            x1, y1, x2, y2 = int(face[0] * img_width), int(face[1] * img_height), \
                     int(face[2] * img_width), int(face[3] * img_height)
            label, emotion_probability=self.predict(image[y1:y2, x1:x2])
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            text = label+" {:.2f}".format(emotion_probability)
            cv2.putText(image, text, (int(face[0] * img_width), int(face[1] * img_height)),
                 cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))
        return image
    def json(self,image):
        img_height, img_width, _ = image.shape
        res=[]
        faces=self.retina.predict(image)
        for face in faces:
            x1, y1, x2, y2 = int(face[0] * img_width), int(face[1] * img_height), \
                     int(face[2] * img_width), int(face[3] * img_height)
            label, emotion_probability=self.predict(image[y1:y2, x1:x2])
            res.append({'box': {
                    "start point": (x1,y1),
                    "end point": (x2,y2)
                },

                    'emotion': label,
                    'probability':str(emotion_probability)
                    })
        return res

