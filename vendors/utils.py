import uuid
from django.core.mail import send_mail
from django.utils.text import slugify
from .models import Hotel

from django.conf import settings
import random

def generate_random_token():
    return str(uuid.uuid4())
    
def send_vendor_email_verification(email, token):
    subject = "Email verification"
    message = f'''Please verify your email by clicking the below link
http://127.0.0.1:8000/vendors/vendor-email-verify/{token}'''
    
    send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
)
    
def generate_otp():
    otp = random.randint(1000, 9999)
    return otp

def send_email_otp(email, otp):
    subject = "OTP verification"
    message = f'''Please use this OTP for verification

{otp}'''
    
    send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
)
    
def generate_slug(hotel_name):
    slug = slugify(hotel_name) + '-' + str(uuid.uuid4()).split('-')[0]
    # check if slug already exists
    if Hotel.objects.filter(hotel_slug=slug).exists():
        return generate_slug(hotel_name)
    return slug
