import os
from django.shortcuts import render

from images.models import Image

from django.conf import settings

from AWS.images import upload_image

def index(request):
    context = {
        'title': 'Nuevo archivo'
    }

    if request.method == 'POST':
        file = request.FILES['file']
        extension = get_extension(file._name)

        local_path = upload_file(file)
        if local_path:
            response = upload_image(settings.BUCKET, local_path, file._name)

            # image = Image.objects.create(
            #     clave=,
            #     bucket=settings.BUCKE,
            #     name=file._name,
            #     size=file.size,
            #     content_type=file.content_type,
            #     extension=extension
            # )
            
            print('La respuesta es: ')
            print(response)

            #delete_file(file._name)
            
    return render(
        request, 
        'index.html', 
        context
    )

def get_extension(name):
    return name.split('.')[-1]

# def delete_file(local_path):
#     os.remove(local_path)

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
