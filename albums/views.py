from django.shortcuts import render
from django.http import JsonResponse

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.views.decorators.csrf import csrf_exempt

from .models import Album

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = self.get_object().title
        context['image'] = self.get_object().images.first()
        context['images'] = self.get_object().images

        return context

@csrf_exempt
def create(request):
    if request.method == 'POST' and request.POST.get('title'):
        
        album = Album.objects.create_by_aws('livedjango', request.POST['title'],
                                            request.POST.get('description', ''))
        
        if album:
            return JsonResponse({'success': True, 'album': album.serializer })
    
    return JsonResponse({'success': False})