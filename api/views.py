from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse,StreamingHttpResponse,HttpResponseServerError
from api.cnn.Models import pad_input_image,recover_pad_output,draw_bbox_landm,draw_bbox_emotion,RetinaFace,Xception
import cv2
import numpy as np
import base64
import json
import requests
from api.camera import VideoCamera
from django.views.decorators import gzip
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django import forms
import tensorflow as tf
from django.core.cache import cache
model_cache_key = 'model_cache'
model_rel_path = "api/cnn/retina_model"

model = cache.get(model_cache_key)

if model is None:
    model_path = os.path.realpath(model_rel_path)
    model = joblib.load(model_path)
    #save in django memory cache
    cache.set(model_cache_key, model, None)

    
#model=RetinaFace()
emotion_classifier=Xception()

def index(request):
    
    
    return render(request, 'api/index.html')


@csrf_exempt
def predict(request):
    if len(request.FILES)==0:
        return HttpResponse(" Please Choose a file",status=404)
    uploaded_file = request.FILES['file']
    content_type = uploaded_file.content_type.split('/')[0]
    if content_type in settings.UPLOAD_EXTENSIONS:
        if uploaded_file.size > settings.MAX_CONTENT_LENGTH:
            return HttpResponse(('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_CONTENT_LENGTH), filesizeformat(uploaded_file.size)),status=500)
    else:
        return HttpResponse('File type is not supported',status=500)
    pass
    
    img_raw = cv2.imdecode(np.fromstring(uploaded_file.read(),
                                     np.uint8), cv2.IMREAD_UNCHANGED)
    img_height_raw, img_width_raw, _ = img_raw.shape
    img = np.float32(img_raw.copy())
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # pad input image to avoid unmatched shape problem
    img, pad_params = pad_input_image(img, max_steps=max([8, 16, 32]))

    outputs = model(img[np.newaxis, ...]).numpy()

    # recover padding effect
    outputs = recover_pad_output(outputs, pad_params)
    json=[]
    for prior_index in range(len(outputs)):
        draw_bbox_emotion(img_raw, outputs[prior_index], img_height_raw,
                                img_width_raw,json,emotion_classifier)
        img = image_resize(img_raw, width=600)
        _, jpeg = cv2.imencode('.jpg', img)
        img = base64.encodebytes(jpeg.tobytes())
    context = {'image': img.decode('utf-8'), 'json': json,'total':len(outputs)}
    return JsonResponse(context, safe=False)

    


@csrf_exempt
def faces(request):
    if len(request.FILES)==0:
        return HttpResponse(" Please Choose a file",status=404)
    uploaded_file = request.FILES['file']
    
    content_type = uploaded_file.content_type.split('/')[0]
    if content_type in settings.UPLOAD_EXTENSIONS:
        if uploaded_file.size > settings.MAX_CONTENT_LENGTH:
            return HttpResponse(('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_CONTENT_LENGTH), filesizeformat(uploaded_file.size)),status=500)
    else:
        return HttpResponse('File type is not supported',status=500)
    pass
    img = cv2.imdecode(np.fromstring(uploaded_file.read(),
                                     np.uint8), cv2.IMREAD_COLOR)
    
    img_height_raw, img_width_raw, _ = img_raw.shape
    img = np.float32(img_raw.copy())
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # pad input image to avoid unmatched shape problem
    img, pad_params = pad_input_image(img, max_steps=max([8, 16, 32]))

    outputs = model(img[np.newaxis, ...]).numpy()

    # recover padding effect
    outputs = recover_pad_output(outputs, pad_params)
    json=[]
    for prior_index in range(len(outputs)):
        draw_bbox_landm(img_raw, outputs[prior_index], img_height_raw,
                                img_width_raw,json)
        img = image_resize(img_raw, width=600)
        _, jpeg = cv2.imencode('.jpg', img)
        img = base64.encodebytes(jpeg.tobytes())
    
    context = {'image': img.decode('utf-8'), 'json':json,'total':len(outputs)}
    return JsonResponse(context, safe=False)


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


    