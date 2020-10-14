from django.urls import path

from .views import show
from .views import delete
from .views import create
from .views import update
from .views import download
from .views import ImageDetailView

app_name = 'images'

urlpatterns = [
    path('<int:pk>', ImageDetailView.as_view(), name='detail'),
    path('create', create, name='create'),
    path('show/<int:pk>', show, name='show'),
    path('delete/<int:pk>', delete, name='delete'),
    path('update/<int:pk>', update, name='update'),
    path('download/<int:pk>', download, name='download')
]