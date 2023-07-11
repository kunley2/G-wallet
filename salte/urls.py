from django.urls import path
from . import views


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user,name='user'),
    path('account/', views.register_account,name='create_account'),
    path('face/', views.face_validation,name='register'),
]