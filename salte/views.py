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
            form.save()
            messages.success(request,'account created successfully')
            return HttpResponseRedirect(reverse('index'))
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)

    form = RegisterUserForm()
    context = {'form':form}
    return render(request,'salte/user/signup.html',context)

def activate_email(request,uidb64,token):
    return HttpResponseRedirect(reverse('create_account'))

def register_account(request):
    
    if request.method == "POST":
        image_path = request.POST["photo"]  # src is the name of input attribute in your html file, this src value is set in javascript code

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
        form = AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request, f"you are now logged in as {username}")
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.error(request,"Invalid username or password.")
                return HttpResponseRedirect(reverse('login'))
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    form = AuthenticationForm()
    context = {'form':form}
    return render(request,'salte/user/login.html',context)

def logout_user(request):
    logout(request)
    messages.success(request,'You have successfully logout')
    return HttpResponseRedirect(reverse("index"))

def forgot_password(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user = User.objects.filter(Q(user_name=user_name)|Q(email=user_name)).first()
        print(user)
        if not user:
            messages.error(request,'No User Found')
            return HttpResponseRedirect(reverse('login'))
        # token = str(uuid.uuid4())
        token = default_token_generator.make_token(user)
        value = send_forgot_password_email(user,token)
        if value:
            messages.success(request,'Email sent')
        return HttpResponseRedirect(reverse('login'))

    return render(request)

def reset_password(request):

    return render(request)

def face_validation(request):
    image1 = cv2.imread(os.path.join(STATIC_DIR,f"salte/images/kunle2.jpg"))
    image2 = cv2.imread(os.path.join(MEDIA_DIR,f"images/kunle_kW6kePB.png"))
    print('image2',image2.shape)
    print('image1',image1.shape)
    img1 = get_face_encoding(image1)
    img2 = get_face_encoding(image2)
    value = face_verification(img2,img1)
    print(value)
    return render(request,'salte/face_recog.html')
