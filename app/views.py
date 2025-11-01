from django.shortcuts import render
from django.http import HttpResponse
from app.models import *
from django.core.mail import send_mail

# 🏠 Amazon Base Page
def amazon(request):
    return render(request, 'amazon.html')


# 📝 Register View
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import User
import random

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        psw = request.POST.get('password')
        uotp = request.POST.get('otp')  # user entered OTP

        # If user already received an OTP and now entered one
        if uotp:
            # compare OTP entered with OTP saved in session
            if uotp == request.session.get('otp'):
                CUO = User.objects.get_or_create(email=email, password=psw)
                if CUO[1]:
                    return HttpResponse("✅ Registered Successfully!")
                else:
                    return HttpResponse("⚠️ User Already Exists!")
            else:
                return HttpResponse("❌ Incorrect OTP!")

        # If user just submitted email & password first time
        else:
            num = str(random.randint(1000, 9999))
            send_mail(
                subject='Hello User,Welcome to amazon😎 ',
                message=f'Welcome to Amazon. Your OTP is {num}.',
                from_email='prawin7396@gmail.com',  # same as EMAIL_HOST_USER in settings.py
                recipient_list=[email],
                fail_silently=False,
            )

            # store info temporarily in session
            request.session['otp'] = num
            request.session['email'] = email
            request.session['password'] = psw

            return render(request, 'register.html', {'otp_sent': True, 'email': email})

    return render(request, 'register.html')



# 🔐 Login View
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        psw = request.POST.get('password')

        UGO = User.objects.filter(email=email, password=psw)
        if UGO:
            return render(request, 'main.html')
        else:
            return HttpResponse("❌ Invalid Credentials! Please Register First.")

    return render(request, 'login.html')


# 🏡 Home View
def home(request):
    return render(request, 'home.html')



