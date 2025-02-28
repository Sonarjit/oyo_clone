from django.shortcuts import render,redirect,HttpResponse
from .models import HotelUser
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .utils import generate_random_token, send_email_verification, send_email_otp, generate_otp
from django.contrib.auth.decorators import login_required

def login_user(request):
    if request.method == 'POST':
        email_id = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user = HotelUser.objects.filter(email=email_id)

        if not hotel_user.exists():
            messages.warning(request, 'Invalid credentials')
            return redirect('user-login')
        
        if not hotel_user[0].is_verified:
            messages.warning(request, "Account not verified")
            return redirect('user-login')
        
        user = authenticate(request, username=hotel_user[0].phone_number, password=password)
        if user is not None:
            login(request , user)
            return redirect('user-dashboard')
        messages.warning(request, "Invalid credentials")
        return redirect('user-login')
    return render(request, 'login.html')

@login_required(login_url='user-login')
def logout_user(request):
    logout(request)
    return redirect('user-login')

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
            return redirect('user-register')

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
        return redirect('user-register')
    
    return render(request, 'register.html')

def verify_email(request, token):
    hotel_user = HotelUser.objects.filter(email_token=token).first()
    try:
        hotel_user = HotelUser.objects.get(email_token=token)
        hotel_user.is_verified = True
        hotel_user.save()
        messages.success(request, "Email verified")
        return redirect('user-login')
    except HotelUser.DoesNotExist:
        return HttpResponse("Invalid Token")

def login_with_otp(request):
    if request.method == 'POST':
        email_id = request.POST.get('email')

        hotel_user = HotelUser.objects.filter(email=email_id)

        if not hotel_user.exists():
            messages.warning(request, 'Invalid credentials')
            return redirect('user-otp-login')
        
        if not hotel_user[0].is_verified:
            messages.warning(request, "Account not verified")
            return redirect('user-otp-login')
        
        if hotel_user[0] is not None:
            otp = generate_otp()
            send_email_otp(email_id, otp)
            hotel_user.update(otp=otp)
            messages.success(request, "Login OTP sent to registered email")
            return redirect(f'/users/user-otp-enter/{email_id}')
        messages.warning(request, "Invalid credentials")
        return redirect('user-otp-login')
    return render(request, 'otp_login.html')

def otp_enter(request, email_id):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        hotel_user = HotelUser.objects.filter(email=email_id)

        if hotel_user.first().otp==otp:
            login(request , hotel_user[0])
            hotel_user.update(otp=None)
            return redirect('user-dashboard')
        messages.warning(request, "Wrong OTP")
        return redirect(f'/users/user-otp-enter/{email_id}')
    return render(request, 'otp_enter.html')

@login_required(login_url='user-login')
def user_dashboard(request):
    return render(request, 'user_dashboard.html')