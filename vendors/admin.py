from django.contrib import admin

# Register your models here.
# admin.py

from .models import *
admin.site.register(HotelVendor)

admin.site.register(Ameneties)