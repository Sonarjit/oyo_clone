from django.urls import path
from . import views

urlpatterns = [
    path('vendor-register/', views.vendor_register, name='vendor-register'),
    path('vendor-login/', views.vendor_login, name='vendor-login'),
    path('vendor-logout/', views.vendor_logout, name='vendor-logout'),
    path('vendor-email-verify/<token>/', views.vendor_verify_email, name='vendor-email-verify'),
    path('vendor-otp-login/', views.vendor_login_with_otp, name='vendor-otp-login'),
    path('vendor-otp-enter/<email_id>/', views.vendor_otp_enter, name='vendor-otp-enter'),
    path('vendor-dashboard/', views.vendor_dashboard, name='vendor-dashboard'),
    path('add-hotel/', views.add_hotel, name='add-hotel'),
]