
import os
import numpy as np
import tensorflow as tf


from api.cnn.Retina.modules.models import RetinaFaceModel
from api.cnn.Retina.modules.utils import load_yaml

def model():
    cfg = load_yaml('api/cnn/Retina/retinaface_mbv2.yaml')
    # define network
    model = RetinaFaceModel(cfg, training=False, iou_th=0.4,
                            score_th=0.5)

    # load checkpoint
    checkpoint_dir = 'api/cnn/Retina/checkpoints/' + cfg['sub_name']
    checkpoint = tf.train.Checkpoint(model=model)
    if tf.train.latest_checkpoint(checkpoint_dir):
        checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))
        print("[*] load ckpt from {}.".format(
            tf.train.latest_checkpoint(checkpoint_dir)))
    else:
        print("[*] Cannot find ckpt from {}.".format(checkpoint_dir))
        exit()
    return model