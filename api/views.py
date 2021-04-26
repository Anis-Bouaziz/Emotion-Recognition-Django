from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse,StreamingHttpResponse,HttpResponseServerError
from api.cnn.models import predict_emotion, detect_faces
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
font = cv2.FONT_HERSHEY_SIMPLEX




    

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
    
    img = cv2.imdecode(np.fromstring(uploaded_file.read(),
                                    np.uint8), cv2.IMREAD_COLOR)
    res=predict_emotion(img)
    faces = json.loads(res.content)
    for face in faces:
        
        x, y, w, h = face['box'].values()
        cv2.putText(img, face['emotion']+' '+face['probability'][:4],
                    (x, y-10), font, 0.75, (0, 0, 255), 2)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
    img = image_resize(img, width=600)
    _, jpeg = cv2.imencode('.jpg', img)
    img = base64.encodebytes(jpeg.tobytes())
    context = {'image': img.decode('utf-8'), 'json': faces,'total':len(faces)}
    del img 
    del jpeg
    del uploaded_file
    del faces
    return JsonResponse(context, safe=False)
    


@csrf_exempt
def faces(request):
    if len(request.FILES)==0:
        return HttpResponse(" Please Choose a file",status=404)
    uploaded_file = request.FILES['file']
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
    
    res = detect_faces(img)
    faces = json.loads(res.content)
    for face in faces:
        x, y, w, h = face['box'].values()
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        for t in face['landmarks'].values():

            cv2.circle(img, tuple(t), 3, (0, 0, 255), -1)
    img = image_resize(img, width=600)
    _, jpeg = cv2.imencode('.jpg', img)
    img = base64.encodebytes(jpeg.tobytes())
    
    context = {'image': img.decode('utf-8'), 'json': faces,'total':len(faces)}
    del img 
    del jpeg
    del uploaded_file
    del faces
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

@csrf_exempt
def video_feed(request):
    if len(request.FILES)==0:
        return HttpResponse(" Camera is off",status=404)
    uploaded_file = request.FILES['file']
    img = cv2.imdecode(np.fromstring(uploaded_file.read(),
                                     np.uint8), cv2.IMREAD_UNCHANGED)
    res= predict_emotion(img)                           
    faces = json.loads(res.content)                                 
    context = {'json': faces,'total':len(faces)}
    del img 
    del jpeg
    del uploaded_file
    del faces
    return JsonResponse(context, safe=False)
    