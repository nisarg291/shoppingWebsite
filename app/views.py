from django.http.response import BadHeaderError
from django.shortcuts import render
import random
# Create your views here.
from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model,login,logout
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Notification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_text,force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail.message import EmailMultiAlternatives
from .token import account_activation_token
from .models import UserOTP
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.
User=get_user_model()
from django.contrib.auth.hashers import check_password
def dj_login(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        print(email)
        print(password)
        user=authenticate(email=email,password=password)
        print('================',user)
        if user:
            login(request,user)
            usr = User.objects.get(email=email)
            print(usr)
            usr_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=usr, otp=usr_otp)
            mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"
            send_mail(
                "Welcome to Nisarg - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently=False,
            )
            return render(request,"otpverify.html",{'usr':usr})
        return render(request,"login.html")
            
    else:
        return render(request,"login.html")

def otpverify(request):
    get_otp = request.POST.get('otp')  # 213243 #None
    if get_otp:
        get_usr = request.POST.get('usr')
        usr = User.objects.get(email=get_usr)
        if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
            usr.is_active = True
            usr.save()
            messages.success(request, f'Account is Created For {usr.email}')
            return redirect('home')
        else:
            messages.warning(request, f'You Entered a Wrong OTP')
            return render(request, 'login.html', {'otp': True, 'usr': usr})
def resend_otp(request):
    if request.method == "GET":
        get_usr = request.GET['usr']
        if User.objects.filter(username=get_usr).exists() and not User.objects.get(username=get_usr).is_active:
            usr = User.objects.get(username=get_usr)
            usr_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=usr, otp=usr_otp)
            mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

            send_mail(
                "Welcome to ITScorer - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently=False
            )
            return HttpResponse("Resend")

    return HttpResponse("Can't Send ")

def register(request):
    alert={}
    if request.method=='POST' and not request.user.is_authenticated:
        first_name=request.POST.get('fname')
        last_name=request.POST.get('lname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(password)
        confirm_password=request.POST.get('confirm_password')
        user=User.objects.create_user(email=email,first_name=first_name,last_name=last_name,password=password,is_active=False)
        try:
            mail_subject="Activate your account"
            current_site=get_current_site(request)
            html_content=render_to_string('acc_active_email.html',{'user':user,'name':first_name+' '+last_name,'email':email,'domain':current_site.domain,'uid':urlsafe_base64_encode(force_bytes(user.pk)),'token':account_activation_token.make_token(user),})
            to_email=user.email
            from_email="parthacademyucmas@gmail.com"
        #msg = f"Hello {user.first_name},\nYour OTP is {user_otp}\nThanks!"
            msg=EmailMultiAlternatives(mail_subject,mail_subject,from_email,to=[to_email])
            msg.attach_alternative(html_content,"text/html")
            msg.send()
            
        except BadHeaderError:
            new_registered_usr=User.objects.get(email__exact==email).delete()
            alert['message']="email not send";
        return activate_account_confirmation(request,first_name+' '+last_name,email)
    else:
        if request.user.is_authenticated:
            if request.user.is_candidate:
                return redirect("home")
            return  render(request)
        # send_mail(
        #         "Welcome to ITScorer - Verify Your Email",
        #         msg,
        #         settings.EMAIL_HOST_USER,
        #         [usr.email],
        #         fail_silently=False
        # )
    return render(request,'register.html')
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
         
               
        return render(request, 'login.html')
    else:
        return HttpResponse('Activation link is invalid!')


def activate_account_confirmation(request,name,email):
    context={'email':email,'name':name}
    return render(request,'activate_account_confirmation.html',context)
    


# @login_required
# def notifications(request):
# 	noti = Notification.objects.filter(user=request.user, seen = False)
# 	noti = serializers.serialize('json', noti)
# 	return JsonResponse({'data':noti})
                     
# @login_required
# def notifications_seen(request):
# 	Notification.objects.filter(user=request.user, seen = False).update(seen = True)
# 	return HttpResponse(True)

# @csrf_exempt
# @login_required
# def clear_notifications(request):
# 	if request.method == "POST":
# 		Notification.objects.filter(user=request.user).delete()
# 		return HttpResponse(True)
# 	return HttpResponse(False)

def islogin(request):
	return JsonResponse({'is_login':request.user.is_authenticated})
                     
                     
def dj_logout(request):
    
    logout(request)
    return render(request,'logout.html')