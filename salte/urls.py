from django.urls import path
from . import views


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user,name='user'),
    # path('activate/<uidb64/<token>', views.,name='activate_email'),
    path('login/', views.login_with_password,name='password_login'),
    path('logout/', views.logout_user,name='logout'),
    path('account/', views.register_account,name='create_account'),
    path('face/', views.face_validation,name='register'),
]