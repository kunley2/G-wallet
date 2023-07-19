from django.shortcuts import render,HttpResponseRedirect
from .face_recog import *
import numpy as np
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q,Sum,Count
from urllib.request import urlopen
from .forms import *
from .models import Account
import random
import cv2


STATIC_DIR = settings.STATIC_DIR
MEDIA_DIR = settings.MEDIA_ROOT


def index(request):

    return render(request, 'salte/index.html')
        
def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.is_active = False
            f.save()
            token = default_token_generator.make_token(f)
            print(token)
            value = activate_account_email(request,f,token)
            messages.success(request,'account created successfully')
            return HttpResponseRedirect(reverse('index'))
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)

    form = RegisterUserForm()
    context = {'form':form}
    return render(request,'salte/user/signup.html',context)

def activate_email(request):
    if request.method == 'POST':
        user_name = request.POST.get('email')
        print(user_name)
        try:
            user = User.objects.get(Q(username=user_name)|Q(email=user_name))
        except:
            messages.error(request,"An Account with the information doesn't exist")
            return HttpResponseRedirect(reverse("activate_email"))
        token = default_token_generator.make_token(user)
        value = activate_account_email(request,user,token)
        messages.success(request,'Please check your email to activate your account')
    return render(request,'salte/user/email_activation.html')


def activate_account(request,uidb64,token):
    id = verify_email_token(uidb64)
    try:
        user = User.objects.get(pk=id)
    except:
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        verified_token = default_token_generator.check_token(user,token)
        user.is_active = True
        user.save()
        messages.success(request,'Email successfully verified')
        return HttpResponseRedirect(reverse("password_login"))
    else:
        messages.error(request,'Unable to verify user')
        print('in else')
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse('create_account'))


def register_account(request):
    
    if request.method == "POST":
        image_path = request.POST["photo"]  # src is the name of input attribute in your html file, this src value is set in javascript code
        print(request.user)

        rand_num = int(str(20) + str(rand_no(8)))
        print(rand_num)
        image = NamedTemporaryFile()
        image.write(urlopen(image_path).read())
        image.flush()
        image = File(image)
        name = str(image.name).split('\\')[-1]
        name = 'kunle.png'  # store image in jpeg format
        image.name = name
        account = Account.objects.create(photo=image)
        account.save()
    # form = CreateAccountForm()
    # context = {'form':form}

    return render(request,'salte/face_recog.html')

def login_with_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user2 = User.objects.get(Q(username=username)|Q(email=username))
            print('user',user2)
        except:
            messages.error(request,'Invalid username or password.')
            return HttpResponseRedirect(reverse('password_login'))
        if user2.is_active != True and user2 != None:
            return HttpResponseRedirect(reverse('activate_email'))
        form = AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            # user = authenticate(email=username, password=password)
            if user is not None:
                login(request,user)
                messages.success(request, f"you are now logged in as {username}")
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.error(request,"Invalid username or password.")
                return HttpResponseRedirect(reverse('password_login'))
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    form = AuthenticationForm()
    context = {'form':form}
    return render(request,'salte/user/login.html',context)


def login_with_face(request):

    return render(request,'salte/user/login_face.html')

def logout_user(request):
    logout(request)
    messages.success(request,'You have successfully logout')
    return HttpResponseRedirect(reverse("index"))

def forgot_password(request):
    if request.method == 'POST':
        user_name = request.POST.get('email')
        user = User.objects.filter(Q(username=user_name)|Q(email=user_name)).first()
        print(user)
        print('user_name',user.username)
        if not user:
            messages.error(request,'No User Found')
            return HttpResponseRedirect(reverse('password_login'))
        # token = str(uuid.uuid4())
        token = default_token_generator.make_token(user)
        value = send_forgot_password_email(user,token)
        if value:
            messages.success(request,'Email sent')
        return HttpResponseRedirect(reverse('password_login'))

    return render(request,'salte/user/password_reset.html')

# def reset_password(request):

#     return render(request)

def face_validation(request):
    # image1 = cv2.imread(os.path.join(STATIC_DIR,f"salte/images/kunle2.jpg"))
    # image2 = cv2.imread(os.path.join(MEDIA_DIR,f"images/kunle_kW6kePB.png"))
    # print('image2',image2.shape)
    # print('image1',image1.shape)
    # img1 = get_face_encoding(image1)
    # img2 = get_face_encoding(image2)
    # value = face_verification(img2,img1)
    # print(value)
    return render(request,'salte/face_recog.html')



###  AJAX REQUEST

def ajax_login_face(request):
     
    is_ajax = request.headers.get('X-Requested-With') == "XMLHttpRequest"
    if is_ajax:
        print('request',request.POST)
        email = request.POST.get('email')
        print(email)
        try:
            user = Account.objects.get(user__email=email)
        except:
            return JsonResponse({'success':False,'message':'User Not registered'})
        print(user)
        return JsonResponse({'success':False})