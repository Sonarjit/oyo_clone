from django.shortcuts import render,redirect,HttpResponse
from .models import HotelUser
from django.db.models import Q
from django.contrib import messages
from .utils import generate_random_token, send_email_verification
from django.contrib.auth import authenticate, login, logout

def login_user(request):
    if request.method == 'POST':
        email_id = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user = HotelUser.objects.filter(email=email_id)

        if not hotel_user.exists():
            messages.warning(request, 'Invalid credentials')
            return redirect('login')
        
        if not hotel_user[0].is_verified:
            messages.warning(request, "Account not verified")
            return redirect('login')
        
        user = authenticate(request, username=hotel_user[0].phone_number, password=password)
        if user is not None:
            # messages.success(request, "Login Success")
            login(request , user)
            return redirect('home')
        messages.warning(request, "Account not verified")
        return redirect('login')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_id = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        
        hotel_user = HotelUser.objects.filter(Q(email=email_id) | Q(phone_number=phone_number))

        if hotel_user.exists():
            messages.warning(request, 'User already exists')
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

        send_email_verification(email_id, hotel_user.email_token)
        messages.success(request, 'User created successfully. Please varify your email')
        return redirect('register')
    
    return render(request, 'register.html')

def verify_email(request, token):
    hotel_user = HotelUser.objects.filter(email_token=token).first()
    try:
        hotel_user = HotelUser.objects.get(email_token=token)
        hotel_user.is_verified = True
        hotel_user.save()
        messages.success(request, "Email verified")
        return redirect('login')
    except HotelUser.DoesNotExist:
        return HttpResponse("Invalid Token")

def otp_authentication(request):
    return render(request, 'otp_authen.html')
