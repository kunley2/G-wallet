import cv2
import dlib
import os
import numpy as np
from django.conf import settings
from django.core.exceptions import ValidationError


STATIC_DIR = settings.STATIC_DIR

face_capture = dlib.get_frontal_face_detector() # this uses dlib library to detect the face
shape_predictor = dlib.shape_predictor(os.path.join(STATIC_DIR,"salte/models/shape_predictor_68_face_landmarks.dat")) # this is used to get the shape of the face
face_recognition_model = dlib.face_recognition_model_v1(os.path.join(STATIC_DIR,'salte/models/dlib_face_recognition_resnet_model_v1.dat')) # this is used to encode the face landmarks
tolerance = 0.58


def get_face_encoding(image):
    
    """ this is used to get the face encoding and names for the different images placed in a folder with the faces name as folder name"""
    encoding = []
    # image = cv2.resize(image,(700,700))
    rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    rect = face_capture(rgb,0)
    print('rect',list(rect))
    if len(rect) > 1:
        raise ValidationError('More Than One Face in the Camera')
    else:
        face_shape = [shape_predictor(image,shape) for shape in rect]
        encodings = [(face_recognition_model.compute_face_descriptor(image,face,1))for face in face_shape]
        # print('encodings',encodings.shape)
        return np.array(encodings)


def face_verification(array1,array2):
    value = np.linalg.norm(array1 - array2) <= tolerance
    return value