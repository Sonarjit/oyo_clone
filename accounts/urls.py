from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('email-verify/<token>/', views.verify_email, name='email-verify'),
    path('otp-login/', views.login_with_otp, name='otp-login'),
    path('otp-enter/<email_id>/', views.otp_enter, name='otp-enter'),
]