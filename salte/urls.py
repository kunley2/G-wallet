from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user,name='user'),
    # path('activate/<uidb64/<token>', views.,name='activate_email'),
    path('login/', views.login_with_password,name='password_login'),
    path('logout/', views.logout_user,name='logout'),
    path('password_reset/', views.lo,name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetCompleteView(template_name='salte/user/reset_confirmation'),name='password_reset_complete'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView(template_name='salte/user/confirm_password.html',),name='password_reset_confirm'),
    path('account/', views.register_account,name='create_account'),
    path('face/', views.face_validation,name='register'),
]