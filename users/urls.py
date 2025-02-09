from django.urls import path
from . import views

urlpatterns = [
    path('user-register/', views.register, name='user-register'),
    path('user-login/', views.login_user, name='user-login'),
    path('user-logout/', views.logout_user, name='user-logout'),
    path('user-email-verify/<token>/', views.verify_email, name='user-email-verify'),
    path('user-otp-login/', views.login_with_otp, name='user-otp-login'),
    path('user-otp-enter/<email_id>/', views.otp_enter, name='user-otp-enter'),
]