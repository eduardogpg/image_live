from django.shortcuts import render
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from .models import Album

@csrf_exempt
def create(request):
    
    if request.method == 'POST' and request.POST.get('title'):
        
        album = Album.objects.create_by_aws('livedjango', request.POST['title'],
                                            request.POST.get('description', ''))
        
        if album:
            return JsonResponse({'success': True, 'album': album.serializer })
    
    return JsonResponse({'success': False})