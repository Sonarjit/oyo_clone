from django.shortcuts import render,redirect,HttpResponse
from django.db.models import Q
from django.contrib import messages
from .utils import generate_random_token, send_email_otp, generate_otp, send_vendor_email_verification
from django.contrib.auth import authenticate, login, logout
from .models import HotelVendor


def vendor_login(request):
    if request.method == 'POST':
        email_id = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user = HotelVendor.objects.filter(email=email_id)

        if not hotel_user.exists():
            messages.warning(request, 'Invalid credentials')
            return redirect('vendor-login')
        
        if not hotel_user[0].is_verified:
            messages.warning(request, "Account not verified")
            return redirect('vendor-login')
        
        user = authenticate(request, username=hotel_user[0].phone_number, password=password)
        if user is not None:
            login(request , user)
            return redirect('home')
        messages.warning(request, "Invalid credentials")
        return redirect('vendor-login')
    return render(request, 'vendor_login.html')

def vendor_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_id = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        business_name = request.POST.get('business_name')
        password = request.POST.get('password')
        
        hotel_user = HotelVendor.objects.filter(Q(email=email_id) | Q(phone_number=phone_number))

        if hotel_user.exists():
            messages.warning(request, 'User already exists')
            return redirect('vendor-register')

        hotel_user = HotelVendor.objects.create(
            username = phone_number,
            first_name = first_name,
            last_name = last_name,
            email = email_id,
            phone_number = phone_number,
            email_token = generate_random_token()
        )
        hotel_user.set_password(password)
        hotel_user.save()

        send_vendor_email_verification(email_id, hotel_user.email_token)
        messages.success(request, 'User created successfully. Please varify your email')
        return redirect('vendor-register')
    
    return render(request, 'vendor_register.html')

def vendor_verify_email(request, token):
    hotel_user = HotelVendor.objects.filter(email_token=token).first()
    try:
        hotel_user = HotelVendor.objects.get(email_token=token)
        hotel_user.is_verified = True
        hotel_user.save()
        messages.success(request, "Email verified")
        return redirect('vendor-login')
    except HotelVendor.DoesNotExist:
        return HttpResponse("Invalid Token")

def vendor_login_with_otp(request):
    if request.method == 'POST':
        email_id = request.POST.get('email')

        hotel_user = HotelVendor.objects.filter(email=email_id)

        if not hotel_user.exists():
            messages.warning(request, 'Invalid credentials')
            return redirect('vendor-otp-login')
        
        if not hotel_user[0].is_verified:
            messages.warning(request, "Account not verified")
            return redirect('vendor-otp-login')
        
        if hotel_user[0] is not None:
            otp = generate_otp()
            send_email_otp(email_id, otp)
            hotel_user.update(otp=otp)
            messages.success(request, "Login OTP sent to registered email")
            return redirect(f'/vendors/vendor-otp-enter/{email_id}')
        messages.warning(request, "Invalid credentials")
        return redirect('vendor-otp-login')
    return render(request, 'vendor_otp_login.html')

def vendor_otp_enter(request, email_id):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        hotel_user = HotelVendor.objects.filter(email=email_id)

        if hotel_user.first().otp==otp:
            login(request , hotel_user[0])
            hotel_user.update(otp=None)
            return redirect('home')
        messages.warning(request, "Wrong OTP")
        return redirect(f'/vendors/vendor-otp-enter/{email_id}')
    return render(request, 'vendor_otp_enter.html')
