from django.shortcuts import render, redirect

from django.http.response import JsonResponse, Http404
from app.forms.login_form import LoginForm
from app.models import User
from utility.utils import generate_otp
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from datetime  import timedelta
from utility.contants import OTP_TIMEOUT, ALLOWED_LOGIN_ATTEMPT, BLOCKED_TIMEOUT_HRS
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.cache import never_cache



def user_profile(request):
    return render(request, 'auth/user_profile.html')

def user_logout(request):
    logout(request)
    return redirect("user-login")

@never_cache
def user_login(request, msg=""):
    now = timezone.localtime(timezone.now())

    if request.method == "POST":        
        data = request.POST
        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)
        if user is not None:
            # if user is blocked : check after 24hrs
            if user.status == 2:
                timediff = now - user.blocked_datetime # must be above 24hr
                if timediff < timedelta(hours=BLOCKED_TIMEOUT_HRS): # if < 24hrs show error
                    msg = "You have exceeded the maximum number of retries. Please try again after 24 hrs."
                else:
                    # if > 24hrs: send otp again. to verify.
                    new_otp = generate_otp()
                    user.otp = new_otp
                    user.status = 0 # inactive user
                    user.updated_at = now
                    user.blocked_datetime = None
                    user.login_attempt = 0
                    user.refresh_from_db()
                    user.save()
                    send_otp_email(user)
                    return render(request, 'auth/otp_verification.html', {"user_id": user.id})
                
            # if login attempt exceeds : block user if max tries
            if user.login_attempt >= ALLOWED_LOGIN_ATTEMPT:
                msg = "You have exceeded the maximum number of retries. Please try again after 24 hrs"
                user.status = 2 # block user
                user.blocked_datetime = now
                user.refresh_from_db()
                user.save()

            # if user is inactive
            if user.status == 0:
                msg = "Your account is not verified. Please check your email for the one-time password (OTP) and enter it below to verify your account."
                new_otp = generate_otp()
                user.otp = new_otp
                user.updated_at = now
                user.refresh_from_db()
                user.save()
                send_otp_email(user)
                return render(request, 'auth/otp_verification.html', {"user_id": user.id, "msg": msg})
            
            # login if active status
            if user.status == 1:
                user.login_attempt = 0
                user.save()
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                
                return redirect("user-profile")
            
            # increase login count
            user.login_attempt += 1
            user.save()
        else:
            msg = "Invalid Username or Password"

    return render(request, "auth/login.html", {"msg": msg})

@never_cache
def otp_verification(request, user_id):
    try:
        msg = "We have sent a one-time password (OTP) to your email address. Please enter the OTP below to continue."
        now = timezone.localtime(timezone.now())

        if request.method == "POST":
            user = User.objects.get(pk=user_id)

            timediff = now - user.updated_at
            print("otp verification timediff:", str(timediff))

            otp_verify_timeout = timedelta(minutes=OTP_TIMEOUT)        
            
            if user.login_attempt >= ALLOWED_LOGIN_ATTEMPT or user.status == 2:
                msg = "You have exceeded the maximum number of retries. Please try again after 24 hrs"
                return render(request, 'auth/otp_verification.html', {"user_id": user_id, "msg": msg})

            if timediff > otp_verify_timeout:
                user.otp = None
                user.save()
                msg = "Your OTP has expired. Please request a new OTP and enter it below to continue."
                return render(request, 'auth/otp_verification.html', {"user_id": user_id, "msg": msg})
            
            data = request.POST
            otp = data.get("otp")
            if otp == user.otp:
                user.status = 1 # active user
                user.login_attempt = 0
                user.otp = None
                user.blocked_datetime = None
                user.save()
                return redirect("user-profile")
            else:
                user.login_attempt += 1
                user.save()

                msg ="Invalid OTP. Please Try again."

        return render(request, 'auth/otp_verification.html', {"user_id": user_id, "msg": msg})
    except Exception as e:
        print(e)
        raise Http404("You are not allowed!")

def signup(request):
    if request.method == "POST":
        now = timezone.localtime(timezone.now())

        data = request.POST
        forms = LoginForm(data)
        user = User()
        if forms.is_valid():
            obj = User.objects.filter(email=data.get("email"))
            if obj.exists():
                kwargs = {"msg": "Welcome back! Your account already exists. Please log in to get started."}
                return redirect("user-login", **kwargs) 

            otp = generate_otp()
            user.first_name = data.get("fname")
            user.last_name = data.get("lname")
            user.updated_at = now
            user.email = data.get("email")
            user.otp = otp
            user.login_attempt = 0
            user.set_password(data.get("password"))
            user.save()

            send_otp_email(user)
            
            kwargs = {"user_id": user.id}
            return redirect("otp-verification", **kwargs)
                    
    return JsonResponse({"msg": "Invalid request!"})

@never_cache
def resend_otp(request, user_id):
    try:
        if request.method != "POST":
            raise "request not allowed."
        
        now = timezone.localtime(timezone.now())
        user = User.objects.get(pk=user_id)

        if user.login_attempt >= ALLOWED_LOGIN_ATTEMPT:
            msg = "You have exceeded the maximum number of retries. Please try again after 24 hrs"
            user.status = 2 # block user
            user.blocked_datetime = now
            user.save()
            return JsonResponse({"success": True, "msg": msg})
        
        new_otp = generate_otp()
        user.login_attempt += 1
        user.otp = new_otp
        user.updated_at = now
        user.save()
        send_otp_email(user)
        msg = "We have sent a one-time password (OTP) to your email address. Please enter the OTP below to continue."
        return JsonResponse({"success": True, "msg": msg})
    except:
        return JsonResponse({"success": False, "msg": "something went wrong!"})

def send_otp_email(user):
    subject = 'Your one-time password for E-Learning'
    html_message = render_to_string('auth/otp_verification_mail.html', {"user": user, "otp": user.otp})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message, fail_silently=True)
