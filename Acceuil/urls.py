from .views import *
from django.urls import path


urlpatterns = [
    path('', acceuil,name='acceuil'),
    path('connexion/', connexion,name='connexion'),
    path('inscription/', inscription,name='inscription'),
    path('restaurationMDP/', mdpoublie,name='mdpoublie'),
    path('contact/', contacter,name='contacter'),
    path('Dashboard/', Dashboard,name='Dashboard'),
    
    # actions backend
    path('connexion/processus', connexionprocessus,name='connexionprocessus'),
    path('deconnexion/processus', deconnexionprocessus,name='deconnexionprocessus'),
    path('inscription/processus', inscriptionprocessus,name='inscriptionprocessus'),
    path('restaurationMDP/processus', mdpoublieprocessus,name='mdpoublieprocessus'),
    
    # Asynchronisme
    # Dashboard
    path('Dashboard/initialisation',initialisation, name='initialisation'),

    # accident
    path('Dashboard/AjouterAccident/AjouterAccidentProcessus',
         AjouterAccidentProcessus, name='AjouterAccidentProcessus'),
    path('Dashboard/tableauAccident/liste',
         tableauAccidentListe, name='tableauAccidentListe'),

    # incident
    path('Dashboard/AjouterIncident/AjouterIncidentProcessus',
         AjouterIncidentProcessus, name='AjouterIncidentProcessus'),
    path('Dashboard/tableauIncident/liste',
         tableauIncidentListe, name='tableauIncidentListe'),

    # profile
    path('Dashboard/profile/updateProfil', updateProfil, name='updateProfil'),
    path('Dashboard/profile/listeUsers', listeUsers, name='listeUsers'),
    path('Dashboard/profile/updatePass', updatePass, name='updatePass'),
    path('Dashboard/profile/addUser', addUser, name='addUser'),
    
    # appels exterieurs
    path('Dashboard/AjouterAccident', AjouterAccident,name='AjouterAccident'),
    path('Dashboard/AjouterIncident', AjouterIncident,name='AjouterIncident'),
    path('Dashboard/tableauAccident', tableauAccident,name='tableauAccident'),
    path('Dashboard/tableauAction', tableauAction,name='tableauAction'),
    path('Dashboard/profile', profile,name='profile'),
]
