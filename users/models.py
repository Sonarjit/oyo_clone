from django.db import models
from django.contrib.auth.models import User

class HotelUser(User):
    profile_picture = models.ImageField(upload_to="userImages")
    phone_number = models.CharField(max_length=20, unique=True)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = "Hotel User"