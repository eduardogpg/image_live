from django.contrib import admin
from django.urls import path, include

from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),

    path('albums/', include('albums.urls')),
    path('images/', include('images.urls')),
]
