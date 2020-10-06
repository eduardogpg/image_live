from django.shortcuts import render

from .models import Image

def list(request):

    images = Image.objects.all().paginate().order_by('-id')

    context = {
        'title': 'Listado de imagenes',
        'images': images
    }
    
    return render(request, 'images/list.html', context)