from django.db import models
from django.contrib.auth.models import User

class HotelVendor(User):
    phone_number = models.CharField(max_length=20, unique=True)
    business_name = models.CharField(max_length=100, default="")
    profile_picture = models.ImageField(upload_to='vendorImages')
    email_token = models.CharField(max_length=100, blank=True, null=True)
    otp = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        db_table = "Hotel Vendor"


class Ameneties(models.Model):
    name = models.CharField(max_length = 1000)
    icon = models.ImageField(upload_to="amemetiesIcons")
    class Meta:
        db_table = "vendors_ameneties"

    def __str__(self)->str:
        return self.name

class Hotel(models.Model):
    hotel_name  = models.CharField(max_length=100)
    hotel_description = models.TextField()
    hotel_slug = models.SlugField(max_length=100, unique=True)
    hotel_owner = models.ForeignKey(HotelVendor,on_delete=models.CASCADE,related_name="hotels")
    ameneties = models.ManyToManyField(Ameneties)
    hotel_price = models.FloatField()
    hotel_offer_price = models.FloatField()
    hotel_location = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "vendors_hotel"

    def __str__(self)->str:
        return self.hotel_name


class HotelImages(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="hotelImages")
    is_selected = models.BooleanField(default=False)

class HotelManager(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE , related_name = "hotel_managers")
    manager_name = models.CharField(max_length = 100)
    manager_contact = models.CharField(max_length = 100)
