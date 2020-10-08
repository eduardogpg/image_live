from django.urls import path

from .views import create

app_name = 'albums'

urlpatterns = [
    path('create', create, name='create'),
]
