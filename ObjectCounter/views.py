from django.http import HttpResponse
from django.template import loader

def index(request):
    context = {
        "data":"nothing"
        }
    
    template = loader.get_template('index/index.html')
    
    return HttpResponse(template.render(context, request))