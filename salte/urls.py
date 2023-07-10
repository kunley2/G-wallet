from django.urls import path
from . import views


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('face/', views.face_recognition,name='face'),
]