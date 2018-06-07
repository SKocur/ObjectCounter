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

    objects = cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=1)
    
    for (x, y, w, h) in objects:
        cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    try:
        cv2.imwrite(PROJECT_ROOT + file, gray)
    except Exception:
        print(Exception)
    
    return len(objects)

def index(request):
    context = {
        "quantity":"0",
        "result_image": "",
    }
        
    template = loader.get_template('index/index.html')
    
    if request.method == "POST" and request.FILES['input_image']:
        file = request.FILES['input_image']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        
        url_to_file = fs.url(filename)
        
        context['quantity'] = process_file(url_to_file)
        context['result_image'] = url_to_file
    
    return HttpResponse(template.render(context, request))