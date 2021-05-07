from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('emotion', views.emotion, name='emotion'),
    path('faces', views.faces, name='faces'),
    path('attributes',views.attributes, name='attributes'),
    path('mask',views.detect_mask,name='mask'),
    path('OpenCamera/',views.OpenCamera,name='Open'),
    path('CloseCamera',views.CloseCamera,name='Close'),
    path('verify',views.verifyFaces,name='verify'),
    path('camera',views.camera,name='camera'),
    path('Facelogin',views.Facelogin,name='Facelogin'),
    path('Facelogout',views.Facelogout,name='Facelogout'),
    path('Facesignin',views.Facesignin,name='Facesignin'),

]
