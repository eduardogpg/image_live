from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib import messages
from django.http import JsonResponse

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from images.forms import UploadFileForm

from django.views.decorators.csrf import csrf_exempt

from .models import Album
from images.models import Image

class AlbumListView(ListView):
    model = Album
    paginate_by = 10
    template_name = 'albums/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Galería'

        return context

    def get_queryset(self):
        return Album.objects.all()

class AlbumDetailView(DetailView):
    model = Album
    template_name = 'albums/detail.html'

    def ge_defaul_image(self):
        if self.get_object().images:
            return self.get_object().first()
        else:
            return Image.obje

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = self.get_object().title
        context['images'] = self.get_object().images
        context['image_default'] = Image.default()
        context['form'] = UploadFileForm(
            {
                'album_id': self.get_object().id
            }
        )

        return context

def create(request):
    if request.method == 'POST':
        if request.POST.get('title'):
            
            album = Album.objects.create_by_aws('livedjango',
                                                request.POST['title'],
                                                request.POST.get('description', ''))
            
            if album:
                messages.success(request, 'Albúm creado exitosamente.')
                return redirect('albums:detail', album.id)

    messages.error(request, 'No es posible completar la operación.')
    return redirect('albums:list')