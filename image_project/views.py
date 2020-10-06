import os
from django.shortcuts import render

from images.models import Image

def index(request):
    context = { 'title': 'Nuevo archivo' }

    if request.method == 'POST':
        file = request.FILES['file']

        local_path = upload_file(file)
        if local_path:
            
            if Image.objects.create_by_aws(local_path, file):
                context['message'] = 'Imagen procesada exitosamente!'

            delete_file(local_path)
            
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
