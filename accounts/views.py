from django.shortcuts import render,redirect
from .models import HotelUser
from django.db.models import Q
from django.contrib import messages
from .utils import generate_random_token

def login(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_id = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        
        hotel_user = HotelUser.objects.filter(Q(email=email_id) | Q(phone_number=phone_number))

        if hotel_user.exists():
            messages.error(request, 'User already exists')
            return redirect('register')

        hotel_user = HotelUser.objects.create(
            username = phone_number,
            first_name = first_name,
            last_name = last_name,
            email = email_id,
            phone_number = phone_number,
            email_token = generate_random_token()
        )
        hotel_user.set_password(password)
        hotel_user.save()

        messages.success(request, 'User created successfully')
        print("user created")
        return redirect('register')
    
    return render(request, 'register.html')

def otp_authentication(request):
    return render(request, 'otp_authen.html')
