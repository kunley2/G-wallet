from django.shortcuts import render
from .face_recog import *
import numpy as np
import os
from django.conf import settings



def index(request):

    return render(request, 'salte/index.html')
        

def face_recognition(request):
    image1 = get_face_encoding('kunle1.jpg')
    image2 = get_face_encoding('kunle2.jpg')
    value = face_verification(image2,image1)
    print(value)

    return render(request,'salte/face_recog.html')
