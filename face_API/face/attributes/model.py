from tensorflow.keras.models import load_model
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array


class FaceAttributes(object):
    def __init__(self,retina):
        self.model=load_model('face_API/face/attributes/weights-FC37-MobileNetV2-0.92.hdf5', compile=False)
        self.retina=retina
        self.attributes=['5_o_Clock_Shadow', 'Arched_Eyebrows','Bags_Under_Eyes', 'Bald' ,'Bangs' ,'Big_Lips','Big_Nose' ,'Black_Hair' ,'Blond_Hair','Brown_Hair', 'Bushy_Eyebrows',
                        'Chubby' ,'Double_Chin' ,'Eyeglasses', 'Goatee' ,'Gray_Hair', 'Heavy_Makeup', 'High_Cheekbones' ,'Male', 'Mouth_Slightly_Open' ,'Mustache' ,'Narrow_Eyes', 'No_Beard' ,'Oval_Face',
                        'Pointy_Nose' ,'Receding_Hairline', 'Rosy_Cheeks', 'Sideburns', 'Smiling', 'Straight_Hair' ,'Wavy_Hair' ,'Wearing_Earrings', 'Wearing_Hat' ,'Wearing_Lipstick',
                        'Wearing_Necklace' ,'Wearing_Necktie' ,'Young'] 
    def __del__(self):
        del self.model
        del self.retina
    def predict(self,face):
        try:
            x=cv2.resize(face,(224,224))
            x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
            x = img_to_array(x) 
            x = x.astype("float") / 255.0
            x = np.expand_dims(x, axis=0)
            preds=self.model.predict(x)[0]
            res = { k:str(v)[:4]   for k, v in zip(self.attributes,preds) if v>0.5}
            return res
        except Exception as e:
            return {}
    def draw(self,image):
        img_height, img_width, _ = image.shape
        faces=self.retina.predict(image)
        for face in faces:
            x1, y1, x2, y2 = int(face[0] * img_width)-30, int(face[1] * img_height)-30, \
                     int(face[2] * img_width)+30, int(face[3] * img_height)+30
            preds=self.predict(image[y1:y2, x1:x2])
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            text=''
            for i,(k,v) in enumerate(preds.items()):
                text =k + ' : '+v
                cv2.putText(image, text, (int(face[0] * img_width)+int(x2-x1)+10, int(face[1] * img_height)+i*20),
                cv2.FONT_HERSHEY_DUPLEX, 0.5, (200, 0, 255))
        return image
    def json(self,image):
        res=[]
        img_height, img_width, _ = image.shape
        faces=self.retina.predict(image)
        for face in faces:
            x1, y1, x2, y2 = int(face[0] * img_width)-30, int(face[1] * img_height)-30, \
                     int(face[2] * img_width)+30, int(face[3] * img_height)+30
            preds=self.predict(image[y1:y2, x1:x2])
            res.append({'box': {
                    "start point": (x1,y1),
                    "end point": (x2,y2)
                },

                    
                    'Attributes':preds
                    })
        return res





