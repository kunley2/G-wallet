from django.shortcuts import render
from .face_recog import *
import numpy as np
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
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
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)

    form = RegisterUserForm()
    context = {'form':form}
    return render(request,'salte/user/signup.html',context)

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
