from django.urls import path

from .views import list

app_name = 'images'


urlpatterns = [
    path('', list, name='list'),
]
