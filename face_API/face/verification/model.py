import cv2
from scipy.spatial.distance import cosine
from face_API.face.verification.vgg16 import RESNET50
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import pickle
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from numpy import load
import os
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
    def createUserModel(self,images):
        data = pickle.loads(open('face_API/face/verification/embeddings.pkl', "rb").read())
        
        for img in images:
            img_height, img_width, _ = img.shape
            face=self.retina.predict(img)
            if len(face)==1:
                face=face[0]
                x1, y1, x2, y2 = int(face[0] * img_width), int(face[1] * img_height), \
                            int(face[2] * img_width), int(face[3] * img_height)
                emb=self.model.predict(preprocess_face(img[y1:y2, x1:x2]))
                data['embeddings'].append(emb[0])
                data['class']=np.append(data['class'],1)
        xtrain ,xtest ,ytrain,ytest=train_test_split(np.asarray(data['embeddings']),np.asarray(data['class']),test_size=0.1)
        recognizer = SVC(C=1.0, kernel="linear", probability=True)
        recognizer.fit(xtrain, ytrain)
        print(recognizer.score(xtest,ytest))
        return pickle.dumps(recognizer)

    def authenticate(self,image,usermodel):
        img_height, img_width, _ = image.shape
        face=self.retina.predict(image)[0]
        x1, y1, x2, y2 = int(face[0] * img_width), int(face[1] * img_height), \
                            int(face[2] * img_width), int(face[3] * img_height)
        embeddings=self.model.predict(preprocess_face(image[y1:y2, x1:x2]))
        usermodel=pickle.loads(usermodel)
        return usermodel.predict(embeddings)[0]
    def create_dataset(self):
        rootdir = 'face_API/face/verification/archive/train'
        data=[]
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                img=cv2.imread(os.path.join(subdir, file))
                
                if img is not None:
                    img_height, img_width, _ = img.shape
                    face=self.retina.predict(img)
                    
                    if len(face)!=0:
                        face=face[0]
                        x1, y1, x2, y2 = int(face[0] * img_width), int(face[1] * img_height), \
                                    int(face[2] * img_width), int(face[3] * img_height)
                        if img[y1:y2, x1:x2].shape[0]!=0:
                            emb=self.model.predict(preprocess_face(img[y1:y2, x1:x2]))
                            data.append(emb[0])
        embeddings={'embeddings':data,'class':np.zeros(len(data))}
        print(embeddings)
        f = open('embeddingd.pkl', "wb")
        f.write(pickle.dumps(embeddings))
        f.close()
        

        


            
            
            
            
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
