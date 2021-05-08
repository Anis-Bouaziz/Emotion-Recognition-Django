
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from keras.models import load_model


class Mask_detection(object):
    def __init__(self,retina):
        try:
            model_path="face_API/face/mask/mask_detector.model"
            self.model= load_model(model_path, compile=False)
            self.retina=retina
        except IOError as e:
            raise e
    def __del__(self):
        del self.model
        del self.retina
    def predict(self,face):
        try:
            Masks = ["ON", "OFF"]
            roi = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            roi = cv2.resize(roi, (224, 224))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            preds = self.model.predict(roi)[0]
            mask_probability = np.max(preds)
            label = Masks[preds.argmax()]
            return label,mask_probability
        except Exception as e:
            return 'None',0.
    def draw(self,image):
        img_height, img_width, _ = image.shape
        faces=self.retina.predict(image)
        for face in faces:
            x1, y1, x2, y2 = int(face[0] * img_width), int(face[1] * img_height), \
                     int(face[2] * img_width), int(face[3] * img_height)
            label ,mask_probability=self.predict(image[y1:y2, x1:x2])
            if label == 'ON':
                color=(0,255,0)
            else:
                color=(0,0,255)
            cv2.rectangle(image, (x1, y1), (x2, y2),color, 2)
            # confidence
            text = label
            cv2.putText(image, text, (int(face[0] * img_width), int(face[1] * img_height)),
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 255))
        return image
    def json(self,image):
        img_height, img_width, _ = image.shape
        res=[]
        faces=self.retina.predict(image)
        for face in faces:
            x1, y1, x2, y2 = int(face[0] * img_width), int(face[1] * img_height), \
                     int(face[2] * img_width), int(face[3] * img_height)
            label ,mask_probability=self.predict(image[y1:y2, x1:x2])
            res.append({'box': {
                        "start point": (x1,y1),
                    "end point": (x2,y2)
                    },

                        'Mask': label,
                        'probability':str(mask_probability)
                        })
        return res

