from django.urls import path,include
from .views import *

urlpatterns = [
    path('formations/', interfaceFormations ,name='interfaceFormations'),
]