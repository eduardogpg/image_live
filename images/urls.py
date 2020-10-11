from django.urls import path

from .views import show
from .views import delete
from .views import ImageDetailView

app_name = 'images'

urlpatterns = [
    path('<int:pk>', ImageDetailView.as_view(), name='detail'),
    
    path('show/<int:pk>', show, name='show'),
    path('delete/<int:pk>', delete, name='delete'),
]