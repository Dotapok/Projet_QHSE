from .views import *
from django.urls import path


urlpatterns = [
    path('', acceuil,name='acceuil'),
    path('connexion/', connexion,name='connexion'),
    path('inscription/', inscription,name='inscription'),
    path('restaurationMDP/', mdpoublie,name='mdpoublie'),
    path('Dashboard/', Dashboard,name='Dashboard'),
    
    # actions backend
    path('connexion/processus', connexionprocessus,name='connexionprocessus'),
    path('inscription/processus', inscriptionprocessus,name='inscriptionprocessus'),
    path('restaurationMDP/processus', mdpoublieprocessus,name='mdpoublieprocessus'),
    
    # Asynchronisme
    
    # appels exterieurs
    path('Dashboard/AjouterAccident', AjouterAccident,name='AjouterAccident'),
    path('Dashboard/tableauAction', tableauAction,name='tableauAction'),
    path('Dashboard/profile', profile,name='profile'),
]
