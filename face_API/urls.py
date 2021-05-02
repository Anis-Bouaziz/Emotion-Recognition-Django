from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('emotion', views.emotion, name='emotion'),
    path('faces', views.faces, name='faces'),
    path('mask',views.detect_mask,name='mask'),
    path('OpenCamera',views.OpenCamera,name='Open'),
    path('CloseCamera',views.CloseCamera,name='Close'),
    path('verify',views.verifyFaces,name='verify'),
    path('camera',views.camera,name='camera'),
]
