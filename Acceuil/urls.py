from .views import *
from django.urls import path


urlpatterns = [
    path('', acceuil,name='acceuil'),
    path('connexion/', connexion,name='connexion'),
    path('inscription/', inscription,name='inscription'),
    path('restaurationMDP/', mdpoublie,name='mdpoublie'),
]
