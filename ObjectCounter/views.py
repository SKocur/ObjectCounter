from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage

from PIL import Image

import os
import cv2
import numpy as np

def process_file(file):
    settings_dir = os.path.dirname(__file__)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))

    # Add additional classifiers based on user input
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(np.array(Image.open(PROJECT_ROOT + file)), cv2.COLOR_BGR2GRAY)

    objects = cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
    
    return len(objects)

def index(request):
    context = {
        "data":"nothing"
        }
    
    template = loader.get_template('index/index.html')
    
    if request.method == "POST" and request.FILES['input_image']:
        file = request.FILES['input_image']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        
        context['data'] = process_file(fs.url(filename))
    
    print(context['data'])
    return HttpResponse(template.render(context, request))