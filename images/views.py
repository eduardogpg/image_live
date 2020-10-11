from django.http import JsonResponse

from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt

from .models import Image

#from .models import Album
from .forms import UploadFileForm

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
            'key': image.key,
        }
    )

@csrf_exempt
def delete(request, pk):
    image = get_object_or_404(Image, pk=pk)
    
    # Owner
    if image.delete():
        return JsonResponse({ 'success': True } )
    else:
        return JsonResponse({ 'success': True } )

def create(request):
    
    albums = Album.objects.all()

    context = { 
        'title': 'Nuevo archivo', 
        'form': UploadFileForm(albums),
    }

    if request.method == 'POST':
        form = UploadFileForm(albums, request.POST, request.FILES)

        if form.is_valid():
            album = get_object_or_404(Album, title=album)

            image = Image.objects.create_by_aws(settings.BUCKET,
                                                form.cleaned_data['file'],
                                                form.cleaned_data['title'], 
                                                form.cleaned_data['album'])

            if image:
                return redirect('albums:detail', album.pk)

        else:
            print('No es valido!!!!')

            
    return render( request, 'index.html', context)
