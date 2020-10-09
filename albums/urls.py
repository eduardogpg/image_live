from django.urls import path

from .views import create
from .views import AlbumListView
from .views import AlbumDetailView

app_name = 'albums'

urlpatterns = [
    path('', AlbumListView.as_view(), name='list'),
    path('detail/<int:pk>', AlbumDetailView.as_view(), name='detail'),
    path('create', create, name='create'),
]
