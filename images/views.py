from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from images.models import Image

from .models import Album
from .forms import UploadFileForm

def create(request):
    
    albums = Album.objects.all()

    context = { 
        'title': 'Nuevo archivo', 
        'form': UploadFileForm(albums),
    }

    if request.method == 'POST':
        form = UploadFileForm(albums, request.POST, request.FILES)

        if form.is_valid():
            
            title = form.cleaned_data['title']
            album = form.cleaned_data['album']
            file = form.cleaned_data['file']

            album = get_object_or_404(Album, title=album)

            image = Image.objects.create_by_aws(settings.BUCKET,
                                                file, title, album)

            if image:
                return redirect('albums:detail', album.pk)

        else:
            print('No es valido!!!!')

            
    return render( request, 'index.html', context)
