import json
import shutil

from pathlib import Path

from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import FileResponse

from django.urls import reverse
from django.conf import settings

from django.contrib import messages

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.http import HttpResponseRedirect

from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt

from .models import Image
from albums.models import Album

from .forms import UploadFileForm

from AWS import download_file

class ImageDetailView(DetailView):
    model = Image
    template_name = 'images/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_object().key

        return context

@csrf_exempt
def show(request, pk):
    image = get_object_or_404(Image, pk=pk)

    return JsonResponse(
        {
            'id': image.id,
            'name': image.name,
            'delete_url': reverse('images:delete', kwargs={'pk': image.id})
        }
    )

def delete(request, pk):
    image = get_object_or_404(Image, pk=pk)
    album = image.album

    if image.delete():
        messages.success(request, 'Imagen eliminada exitosamente.')
    else:
        messages.error(request, 'No fue posible completar la operación')

    return redirect('albums:detail', album.id)

def create(request):
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            album = get_object_or_404(Album, id=form.cleaned_data['album_id'])

            image = Image.objects.create_by_aws(settings.BUCKET,
                                                form.cleaned_data['file'],
                                                album)

            if image:
                messages.success(request, 'Imagen almacenada exitosamente.')
                return redirect('albums:detail', album.pk)
    
    messages.success(request, 'No fue posible completar la operación.')
    
    return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

def update(request, pk):
    image = get_object_or_404(Image, pk=pk)

    if request.method == 'POST' and request.POST.get('name'):
        
        new_name = request.POST['name']
        file_type = image.content_type.split('/')[-1]

        new_name = f'{new_name}.{file_type}'

        if image.update_name(new_name):
            pass

    return redirect('albums:detail', image.album.pk)

def download(request, pk):
    image = get_object_or_404(Image, pk=pk)

    local_path = f'tmp/{image.name}'
    
    if download_file(image.bucket, image.key, local_path):
        return FileResponse(open(local_path, 'rb'))

    raise Http404

@csrf_exempt
def delete_many(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        images_deleted = [Image.objects.delete_by_id(id) for id in payload.get('ids', []) ]

    return JsonResponse(
        { 
            'success': True, 
            'images_deleted': images_deleted,
        }
    )

@csrf_exempt
def download_many(request):
    album = Album.objects.first() # Cambiar por el usuario
    
    zip_path = f'tmp/zip/{album.name}'
    download_path = f'tmp/images/{album.key}'
    
    Path(zip_path).mkdir(parents=True, exist_ok=True)
    Path(download_path).mkdir(parents=True, exist_ok=True)

    if request.method == 'POST':
        payload = json.loads(request.body)

        for id in payload.get('ids', []):
            image = Image.objects.filter(id=id).first()

            if image:
                image_path = f'{download_path}{image.name}'
                download_file(image.bucket, image.key, image_path)
        
        shutil.make_archive(zip_path, 'zip', download_path)

        return FileResponse(open(zip_path + '.zip', 'rb'))

    return JsonResponse( {  'success': False } )