import cv2
import numpy as np
import tensorflow as tf

class RetinaFace(object):
    def __init__(self):
        model_path="face_API/face/detection/retina_model" 
        self.model=tf.saved_model.load(model_path, tags=None, options=None)
    def __del__(self):
        del self.model
    def predict(self,image):
        img_height_raw, img_width_raw, _ = image.shape
        img = np.float32(image.copy())
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # pad input image to avoid unmatched shape problem
        img, pad_params = pad_input_image(img, max_steps=max([8, 16, 32]))
        outputs = self.model(img[np.newaxis, ...]).numpy()
        # recover padding effect
        outputs = recover_pad_output(outputs, pad_params)
        return outputs
    def draw(self,image):
        img_height, img_width, _ = image.shape
        faces=self.predict(image)
        for face in faces:
            # bbox
            x1, y1, x2, y2 = int(face[0] * img_width), int(face[1] * img_height), \
                            int(face[2] * img_width), int(face[3] * img_height)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # confidence
            text = "{:.4f}".format(face[15])
            cv2.putText(image, text, (int(face[0] * img_width), int(face[1] * img_height)),
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))

            # landmark
            if face[14] > 0:
                cv2.circle(image, (int(face[4] * img_width),
                                int(face[5] * img_height)), 1, (255, 0, 0), 2)
                cv2.circle(image, (int(face[6] * img_width),
                                int(face[7] * img_height)), 1, (255, 0, 0), 2)
                cv2.circle(image, (int(face[8] * img_width),
                                int(face[9] * img_height)), 1, (255, 0, 0), 2)
                cv2.circle(image, (int(face[10] * img_width),
                                int(face[11] * img_height)), 1, (255, 0, 0), 2)
                cv2.circle(image, (int(face[12] * img_width),
                                int(face[13] * img_height)), 1, (255, 0, 0), 2)
        return image
    def json(self,image):
        res=[]
        img_height, img_width, _ = image.shape
        faces=self.predict(image)
        for face in faces:
            x1, y1, x2, y2 = int(face[0] * img_width), int(face[1] * img_height), \
                            int(face[2] * img_width), int(face[3] * img_height)
            res.append({'box': {
                    "start point": (x1,y1),
                    "end point": (x2,y2)
                },

                    'landmarks': {
                        "eye_left":(int(face[4] * img_width),int(face[5] * img_height)),
                        "eye_right":(int(face[6] * img_width),int(face[7] * img_height)),
                        "nose":(int(face[8] * img_width), int(face[9] * img_height)),
                        "mouth_left":(int(face[10] * img_width), int(face[11] * img_height)),
                        "mouth_right":(int(face[12] * img_width), int(face[13] * img_height))

                    }
                    }) 
        return res


def pad_input_image(img, max_steps):
        """pad image to suitable shape"""
        img_h, img_w, _ = img.shape

        img_pad_h = 0
        if img_h % max_steps > 0:
            img_pad_h = max_steps - img_h % max_steps

        img_pad_w = 0
        if img_w % max_steps > 0:
            img_pad_w = max_steps - img_w % max_steps

        padd_val = np.mean(img, axis=(0, 1)).astype(np.uint8)
        img = cv2.copyMakeBorder(img, 0, img_pad_h, 0, img_pad_w,
                                cv2.BORDER_CONSTANT, value=padd_val.tolist())
        pad_params = (img_h, img_w, img_pad_h, img_pad_w)

        return img, pad_params

def recover_pad_output(outputs, pad_params):
    """recover the padded output effect"""
    img_h, img_w, img_pad_h, img_pad_w = pad_params
    recover_xy = np.reshape(outputs[:, :14], [-1, 7, 2]) * \
        [(img_pad_w + img_w) / img_w, (img_pad_h + img_h) / img_h]
    outputs[:, :14] = np.reshape(recover_xy, [-1, 14])

    return outputs

    
    