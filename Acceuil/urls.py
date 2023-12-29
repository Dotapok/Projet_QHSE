from django.urls import path,include
from .views import *

urlpatterns = [
    path('acceuil/', acceuil ,name='acceuil'),
]