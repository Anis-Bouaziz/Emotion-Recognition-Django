from django.shortcuts import render , redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse,StreamingHttpResponse
from django.core.exceptions import ValidationError
import cv2
import numpy as np
import base64
import json
from django.views.decorators import gzip
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from face_API.face.detection.model import RetinaFace
from face_API.face.emotions.model import Xception
from face_API.face.mask.model import Mask_detection
from face_API.face.verification.model import FaceVerif
from face_API.face.attributes.model import FaceAttributes
from face_API.camera import VideoCamera
import os
from face_API.auth_backend import PasswordlessAuthBackend
from django.contrib.auth import  login,logout
from face_API.models import CustomUser, CustomUserManager
#Load Models
try:
    Retina=RetinaFace()
    emotion_classifier=Xception(Retina)
    mask_classifier=Mask_detection(Retina)
    attributes_classifier=FaceAttributes(Retina)
    verif= FaceVerif(Retina) 
except IOError as f:
    print('Models were not properly loaded')



def index(request):
    return render(request, 'face_API/index.html')
@csrf_exempt
def faces(request):
    if len(request.FILES)==0:
        return HttpResponse(" Please Choose a file",status=404)
    try:
        validate(request.FILES['file'])
    except ValidationError as v: 
        return HttpResponse(v,400)
    else:
        img_raw = cv2.imdecode(np.fromstring(request.FILES['file'].read(),np.uint8), cv2.IMREAD_COLOR)
        img=Retina.draw(img_raw)
        img = image_resize(img_raw, width=600)
        _, jpeg = cv2.imencode('.jpg', img)
        img = base64.encodebytes(jpeg.tobytes())
        json=Retina.json(img_raw)
        context = {'image': img.decode('utf-8'), 'json':json,'total':len(json)}
        return JsonResponse(context, safe=False)
@csrf_exempt
def emotion(request):
    
    if len(request.FILES)==0:
        return HttpResponse(" Please Choose a file",status=404)
    try:
        validate(request.FILES['file'])
    except ValidationError as v: 
        return HttpResponse(v,400)
    else:
        img_raw = cv2.imdecode(np.fromstring(request.FILES['file'].read(),
                                        np.uint8), cv2.IMREAD_UNCHANGED)
        img=emotion_classifier.draw(img_raw)
        img = image_resize(img_raw, width=600)
        _, jpeg = cv2.imencode('.jpg', img)
        img = base64.encodebytes(jpeg.tobytes())
        json=emotion_classifier.json(img_raw)
        context = {'image': img.decode('utf-8'), 'json': json,'total':len(json)}
        return JsonResponse(context, safe=False)
@csrf_exempt
def detect_mask(request):
       
    if len(request.FILES)==0:
        return HttpResponse(" Please Choose a file",status=404)
    try:
        validate(request.FILES['file'])
    except ValidationError as v: 
        return HttpResponse(v,400)
    else:
        img_raw = cv2.imdecode(np.fromstring(request.FILES['file'].read(),
                                        np.uint8), cv2.IMREAD_UNCHANGED)
        img=mask_classifier.draw(img_raw)
        img = image_resize(img_raw, width=600)
        _, jpeg = cv2.imencode('.jpg', img)
        img = base64.encodebytes(jpeg.tobytes())
        json=mask_classifier.json(img_raw)
        context = {'image': img.decode('utf-8'), 'json': json,'total':len(json)}
        return JsonResponse(context, safe=False)
@csrf_exempt
def attributes(request):
    if len(request.FILES)==0:
        return HttpResponse(" Please Choose a file",status=404)
    if len(request.FILES)==0:
        return HttpResponse(" Please Choose a file",status=404)
    try:
        validate(request.FILES['file'])
    except ValidationError as v: 
        return HttpResponse(v,400)
    else:
        img_raw = cv2.imdecode(np.fromstring(request.FILES['file'].read(),
                                        np.uint8), cv2.IMREAD_UNCHANGED)
        img=attributes_classifier.draw(img_raw)
        img = image_resize(img_raw, width=600)
        _, jpeg = cv2.imencode('.jpg', img)
        img = base64.encodebytes(jpeg.tobytes())
        json=attributes_classifier.json(img_raw)
        context = {'image': img.decode('utf-8'), 'json': json,'total':len(json)}
        return JsonResponse(context, safe=False)
@csrf_exempt
def verifyFaces(request):
    if len(request.FILES)!=2:
            return HttpResponse(" Please Choose 2 Images",status=404)
    uploaded_file1 = request.FILES['file']
    uploaded_file2 = request.FILES['file2']
    try:
        validate(uploaded_file2)
        validate(uploaded_file2)
    except ValidationError as v: 
        return HttpResponse(v,400)
    img_raw1 = cv2.imdecode(np.fromstring(uploaded_file1.read(),
                                        np.uint8), cv2.IMREAD_COLOR)
    img_raw2 = cv2.imdecode(np.fromstring(uploaded_file2.read(),
                                        np.uint8), cv2.IMREAD_COLOR)

    img_height_raw1, img_width_raw1, _ = img_raw1.shape
    img1,img2=verif.draw(img_raw1,img_raw2)
    img1 = image_resize(img_raw1, width=600)
    _, jpeg1 = cv2.imencode('.jpg', img1)
    img1 = base64.encodebytes(jpeg1.tobytes())
    img2 = image_resize(img_raw2, width=600)
    _, jpeg2 = cv2.imencode('.jpg', img2)
    img2 = base64.encodebytes(jpeg2.tobytes())
    json=verif.json(img_raw1,img_raw2)
    context = {'image1': img1.decode('utf-8'),'image2':  img2.decode('utf-8'),'json':json}
    return JsonResponse(context, safe=False)
##########################Authentication################################
@csrf_exempt
def Facesignin(request):
    images=[]
    if len(request.FILES)!=7:
        return HttpResponse('please upload 6 pictures and a profile picture',status=400)
    for f in request.FILES.values():
        try:
            validate(f)
        except ValidationError as v: 
            return HttpResponse(v,400)
        else :
            images.append(cv2.imdecode(np.fromstring(f.read(),np.uint8), cv2.IMREAD_COLOR))
    profilepic=request.FILES['Profilepicture']
    username=request.POST['username']
    email=request.POST['email']
    try:
        user = CustomUser.objects.get(username=username)
        return HttpResponse('User already exists',status=302)
    except CustomUser.DoesNotExist:
        try:
            model=verif.createUserModel(images)
        except FileNotFoundError as e:
            return HttpResponse('could not create user model',500)
        else:
            CustomUser.objects.create_user(email,username,model,profilepic)
            return HttpResponse(200)  
@csrf_exempt
def Facelogin(request):
    auth=PasswordlessAuthBackend()
    img_raw = cv2.imdecode(np.fromstring(request.FILES['file'].read(),np.uint8), cv2.IMREAD_COLOR)
    uname=request.POST['username']
    user = auth.authenticate(username=uname)
    if user:
        try:
            result=verif.authenticate(img_raw,user.UserFile)
            if int(result)==1:
                login(request,user,'face_API.auth_backend.PasswordlessAuthBackend')
                return HttpResponse('logged in ',status=200)
            else:
                return HttpResponse('Wrong user',status=401)
        except ValidationError as e:
            return HttpResponse (e.message,status=401)
    else: 
        return HttpResponse('username not found',status=404)   
@csrf_exempt
def Facelogout(request):
    logout(request)
    return redirect(index)
###########################CAMERA#######################################
os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'

def gen(camera):
    img_array = []
    while camera.grabbed:
        frame = camera.get_frame()
        frame=cameramodel.draw(frame)
        _, jpg = cv2.imencode('.jpg', frame)
        img_array.append(jpg)
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + jpg .tobytes()+ b'\r\n\r\n')
    return HttpResponse(200)
@csrf_exempt
@gzip.gzip_page
def camera(request): 
    camera=VideoCamera()
    if camera.video.isOpened():
        try:
            return StreamingHttpResponse(gen(camera),content_type="multipart/x-mixed-replace;boundary=frame")
        except :
            return
    else : camera.video.release()
@csrf_exempt 
def OpenCamera(request):
    global cameramodel
    m = request.GET.get('mode')
    if m=='1':
        cameramodel=Retina
    elif m=='2':
        cameramodel=emotion_classifier
    elif m=='3':
        cameramodel=mask_classifier
    elif m=='4': 
        cameramodel=attributes_classifier
    else : 
        return HttpResponse(status=401)
    return render(request, 'face_API/camera.html')   
@csrf_exempt  
def CloseCamera(request):
    if request.POST['cam']=='0':
        VideoCamera().video.release()
    return HttpResponse(200)
########################UTILS#############################################
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
def validate(uploaded_file):
    content_type = uploaded_file.content_type.split('/')[0]
    if content_type in settings.UPLOAD_EXTENSIONS:
        if uploaded_file.size > settings.MAX_CONTENT_LENGTH:
            
            raise  ValidationError(('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_CONTENT_LENGTH), filesizeformat(uploaded_file.size)))       
    else:
        raise ValidationError('File type is not supported')


        
        