import cv2
from scipy.spatial.distance import cosine
from face_API.face.verification.vgg16 import RESNET50
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
class FaceVerif(object):
    def __init__(self,retina):
        self.retina=retina
        self.model=RESNET50(include_top=False, input_tensor=None,
                        input_shape=(224, 224, 3), pooling='avg',
                        weights='vggface',
                        classes=8631)
        
    def __del__(self):
        
        del self.retina
    def predict(self,face1,face2):
        emb1=self.model.predict(preprocess_face(face1))
        emb2=self.model.predict(preprocess_face(face2))
        score = cosine(emb1, emb2)
        return score
    def draw(self, image1,image2):
        img1=self.retina.draw(image1)
        img2=self.retina.draw(image2)
        return img1,img2
    def json(self,image1,image2):
        res=[]
        face1=self.retina.predict(image1)
        face2=self.retina.predict(image2)
        if len(face1)==1 and len(face2)==1:
            img_height1, img_width1, _ = image1.shape
            img_height2, img_width2, _ = image2.shape
            face1=face1[0]
            face2=face2[0]
            x1, y1, x2, y2 = int(face1[0] * img_width1), int(face1[1] * img_height1), \
                            int(face1[2] * img_width1), int(face1[3] * img_height1)
            x11, y11, x21, y21 = int(face2[0] * img_width2), int(face2[1] * img_height2), \
                            int(face2[2] * img_width2), int(face2[3] * img_height2)
            score=self.predict(image1[y1:y2, x1:x2],image2[y11:y21, x11:x21])
            
            if score <= 0.5:
                res.append({'result' :'Face is a Match with score of '+str(score)})
            else :
                res.append({'result':'Face is not a Match with score of '+str(score)})
        else:
            res.append({'error' :'each image must contain one face'})
        return res
            
            
            
            
def preprocess_face(face):
    face=cv2.resize(face,(224,224))
    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    face = img_to_array(face)
    face = face[..., ::-1]
    face[..., 0] -= 91.4953
    face[..., 1] -= 103.8827
    face[..., 2] -= 131.0912
    face = np.expand_dims(face, axis=0)
    return face
