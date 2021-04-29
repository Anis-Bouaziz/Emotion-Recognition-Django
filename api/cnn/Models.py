import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow as tf
from tensorflow.keras.models import load_model

class RetinaFace(object):
    def __init__(self):
        #self.session = tf.compat.v1.Session()
        model_path="api/cnn/retina_model" 
        #self.model=tf.saved_model.loader.load(self.session,[tf.saved_model.tag_constants.SERVING],model_path)
        self.model=tf.saved_model.load(model_path, tags=None, options=None)
    # def predict(self, images):
    # predictions = self.session.run(self.model, {'Placeholder:0': images})
    # # TODO: convert to human-friendly labels
    # return predictions   


class Xception:
    def __init__(self):
        model_path="api/cnn/video.h5"
        self.model= load_model(model_path, compile=False)
    


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

def draw_bbox_landm(img, ann, img_height, img_width,json):
    """draw bboxes and landmarks"""
    # bbox
    x1, y1, x2, y2 = int(ann[0] * img_width), int(ann[1] * img_height), \
                     int(ann[2] * img_width), int(ann[3] * img_height)
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # confidence
    text = "{:.4f}".format(ann[15])
    cv2.putText(img, text, (int(ann[0] * img_width), int(ann[1] * img_height)),
                cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))

    # landmark
    if ann[14] > 0:
        cv2.circle(img, (int(ann[4] * img_width),
                         int(ann[5] * img_height)), 1, (255, 0, 0), 2)
        cv2.circle(img, (int(ann[6] * img_width),
                         int(ann[7] * img_height)), 1, (255, 0, 0), 2)
        cv2.circle(img, (int(ann[8] * img_width),
                         int(ann[9] * img_height)), 1, (255, 0, 0), 2)
        cv2.circle(img, (int(ann[10] * img_width),
                         int(ann[11] * img_height)), 1, (255, 0, 0), 2)
        cv2.circle(img, (int(ann[12] * img_width),
                         int(ann[13] * img_height)), 1, (255, 0, 0), 2)
    #json
    json.append({'box': {
                    "top": x1,
                    "left": y1,
                    "width": x2,
                    "height": y2
                },

                    'landmarks': {
                        "eye_left":(int(ann[4] * img_width),int(ann[5] * img_height)),
                        "eye_right":(int(ann[6] * img_width),int(ann[7] * img_height)),
                        "nose":(int(ann[8] * img_width), int(ann[9] * img_height)),
                        "mouth_left":(int(ann[10] * img_width), int(ann[11] * img_height)),
                        "mouth_right":(int(ann[12] * img_width), int(ann[13] * img_height))

                    }
                    })

def draw_bbox_emotion(img, ann, img_height, img_width,json,emotion_classifier):
    """draw bboxes and landmarks"""
    
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

    # confidence
    text = label+" {:.2f}".format(emotion_probability)
    cv2.putText(img, text, (int(ann[0] * img_width), int(ann[1] * img_height)),
                 cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))
    #json
    json.append({'box': {
                    "top": x1,
                    "left": y1,
                    "width": x2,
                    "height": y2
                },

                    'emotion': label,
                    'probability':str(emotion_probability)
                    })
