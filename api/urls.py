from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict', views.predict, name='predictions'),
    path('faces', views.faces, name='faces')
]
