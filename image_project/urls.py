from django.contrib import admin
from django.urls import path, include

from images.views import create

urlpatterns = [
    path('', create, name='index'),
    path('admin/', admin.site.urls),

    path('albums/', include('albums.urls')),
    #path('images/', include('images.urls')),
]
