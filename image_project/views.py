import os
from django.shortcuts import render

from images.models import Image
from albums.models import Album

from images.forms import UploadFileForm

def index(request):
    
    form = UploadFileForm(request.POST or None)

    context = { 
        'title': 'Nuevo archivo', 
        'form': form,
    }
            
    return render( request, 'index.html', context)

def delete_file(local_path):
    os.remove(local_path)

def upload_file(file):
    try:
        local_path = f'tmp/{file}'
        with open(local_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return local_path

    except Exception as err:
        print('No fue posible crear el archivo.')
        print(err)
