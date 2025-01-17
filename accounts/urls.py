from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('email-verify/<token>/', views.verify_email, name='email-verify'),
    path('otp-authentication/', views.otp_authentication, name='otp-authentication'),

]