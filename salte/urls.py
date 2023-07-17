from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.register_user,name='user'),
    path('activate/<uidb64>/<token>', views.activate_account,name='activate_account'),
    path('login/', views.login_with_password,name='password_login'),
    path('face_login/', views.login_with_face,name='face_login'),
    path('logout/', views.logout_user,name='logout'),
    path('password_reset/', views.forgot_password,name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='salte/user/reset_confirmation.html'),name='password_reset_complete'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='salte/user/confirm_password.html',),name='password_reset_confirm'),
    path('account/', views.register_account,name='create_account'),
    path('activate-email/', views.activate_email,name='activate_email'),
    path('face/', views.face_validation,name='register'),
]