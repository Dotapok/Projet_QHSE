from django.urls import path,include
from .views import *

urlpatterns = [
    path('accidents/', interfaceAccidents ,name='interfaceAccidents'),
]