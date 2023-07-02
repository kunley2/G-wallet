from django.shortcuts import render


def index(request):

    return render(request, 'salte/index.html')
        

def face(request):

    return render(request,'salte/face_recog.html')
