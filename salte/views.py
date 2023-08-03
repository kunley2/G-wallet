from django.shortcuts import render,HttpResponseRedirect,redirect
from .helper import *
import numpy as np
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.decorators import login_required
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
            return HttpResponseRedirect(reverse('salte:index'))
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
            return HttpResponseRedirect(reverse("salte:activate_email"))
        token = default_token_generator.make_token(user)
        value = activate_account_email(request,user,token)
        messages.success(request,'Please check your email to activate your account')
    return render(request,'salte/user/email_activation.html')


def activate_account(request,uidb64,token):
    id = verify_email_token(uidb64)
    print(id)
    try:
        user = User.objects.get(pk=id)
    except:
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        verified_token = default_token_generator.check_token(user,token)
        user.is_active = True
        user.save()
        messages.success(request,'Email successfully verified')
        return HttpResponseRedirect(reverse("salte:create_account"))
    else:
        messages.error(request,'Unable to verify user, Please Try again')
        print('in else')
        return HttpResponseRedirect(reverse("salte:activate_email"))
    # return HttpResponseRedirect(reverse('salte:create_account'))

@login_required()
def register_account(request):
    
    if request.method == "POST":
        image_path = request.POST["photo"]  # src is the name of input attribute in your html file, this src value is set in javascript code
        phone_number = request.POST["phone_number"]
        date_of_birth = request.POST["date_of_birth"]
        pwd1 = request.POST["pwd1"]
        pwd2 = request.POST["pwd2"]
        pwd3 = request.POST["pwd3"]
        pwd4 = request.POST["pwd4"]

        passcode = int(str(pwd1) + str(pwd2) + str(pwd3) + str(pwd4) )
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        account_name = first_name + last_name
        rand_num = int(str(20) + str(rand_no(8)))
        image = NamedTemporaryFile()
        image.write(urlopen(image_path).read())
        image.flush()
        image = File(image)
        name = str(image.name).split('\\')[-1]
        name = f'{first_name}.png'  # store image in png format
        image.name = name
        account = Account.objects.create(photo=image,user=request.user,phone_number=phone_number,
                                         date_of_birth=date_of_birth,passcode=passcode,account_number=rand_num,
                                         account_name=account_name)
        if account.save():
            messages.success(request,'Account succesfully created')
            return HttpResponseRedirect(reverse("salte:index"))



    form = CreateAccountForm()
    context = {'form':form}

    return render(request,'salte/account/create_account.html',context)

def login_with_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        next = request.POST.get('next')
        try:
            user2 = User.objects.get(Q(username=username)|Q(email=username))
            print('user2 in search',user2)
        except:
            messages.error(request,'Invalid username or password.')
            return HttpResponseRedirect(reverse('salte:password_login'))
        if user2.is_active != True and user2 != None:
            return HttpResponseRedirect(reverse('salte:activate_email'))
        form = AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print("user in the authenticate",user)
            # user = authenticate(email=username, password=password)
            print('bool',bool(next))
            if user is not None and bool(next) == False:
                login(request,user)
                print('not in the next')
                messages.success(request, f"you are now logged in as {username}")
                return HttpResponseRedirect(reverse('salte:index'))
            elif user is not None and bool(next) == True:
                login(request,user)
                print('next',next)
                messages.success(request, f"you are now logged in as {username}")
                print('in the next none')
                return HttpResponseRedirect(f'{next}')
            else:
                messages.error(request,"Invalid username or password.")
                return HttpResponseRedirect(reverse('salte:password_login'))
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('salte:index'))
    form = AuthenticationForm()
    context = {'form':form}
    return render(request,'salte/user/login.html',context)


def login_with_face(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('salte:index'))
    return render(request,'salte/user/login_face.html')

def logout_user(request):
    logout(request)
    messages.success(request,'You have successfully logout')
    return HttpResponseRedirect(reverse("salte:index"))

def forgot_password(request):
    if request.method == 'POST':
        user_name = request.POST.get('email')
        user = User.objects.filter(Q(username=user_name)|Q(email=user_name)).first()
        print(user)
        print('user_name',user.username)
        if not user:
            messages.error(request,'No User Found')
            return HttpResponseRedirect(reverse('salte:password_login'))
        # token = str(uuid.uuid4())
        token = default_token_generator.make_token(user)
        value = send_forgot_password_email(user,token)
        if value:
            messages.success(request,'Email sent')
        return HttpResponseRedirect(reverse('salte:password_login'))

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


def faqs(request):
    return render(request, 'salte/faqs.html')



###  AJAX REQUEST

def ajax_login_face(request):
     
    is_ajax = request.headers.get('X-Requested-With') == "XMLHttpRequest"
    if is_ajax:
        # print('request',request.POST)
        email = request.POST.get('email')
        query_image = request.POST.get('image')
        print('user account',Account.objects.filter(Q(user__email=email)|Q(user__username=email)))
        try:
            user = Account.objects.get(user__email=email)
        except Exception as e:
            print('error',e)
            return JsonResponse({'success':False,'message':'User Not registered'})
        user_image = user.photo
        user_image = cv2.imread(os.path.join(MEDIA_DIR,str(user.photo)))
        # user_image = cv2.imread(os.path.join(STATIC_DIR,'salte/images/color.jpg'))
        query_image = read_b64_image(query_image)
        print('query size',query_image.size)
        print('user size',user_image.size)
        # cv2.imwrite(os.path.join(STATIC_DIR,'salte/images/color23.jpg'), query_image )
        # cv2.imshow('',query_image)
        # cv2.waitKey(1)
        encoded_user = get_face_encoding(user_image)
        encoded_query = get_face_encoding(query_image)
        print('encoded user',encoded_user)
        print('encoded query',encoded_query)
        try:
            if face_verification(encoded_user,encoded_query):
                print('in the ',User.objects.get(email=email).username)
                logged_user = User.objects.get(email=email)
                # log_user = authenticate(username=)
                # login(request,logged_user.username)
                return JsonResponse({'success':True})
        except Exception as e:
            print('error',e)
        return JsonResponse({'success':False,'message':'Please try again'})
