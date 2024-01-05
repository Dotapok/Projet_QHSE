from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.models import User
import random as Generateur
from django.contrib.auth.decorators import login_required
from Acceuil.models import *
from .forms import *
from django.contrib.auth.hashers import make_password

# Create your views here.
def acceuil(request):
    return render(request,'index.html')

def connexion(request):
    return render(request,'pages-login.html')

def inscription(request):
    return render(request,'register.html')

def mdpoublie(request):
    return render(request,'forgot-password.html')

@login_required(login_url='connexion')
def Dashboard(request):
    return render(request,'dashboard.html')

# fonctionalités
def connexionprocessus(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        
        user = authenticate(request, email=email, password=pwd)
        if user:
            login(request, user)
            redirection_url = '/Dashboard/'
            return JsonResponse({'success': True,'redirection_url': redirection_url})
        else:
            return JsonResponse({'success': False}, status=401)
    return JsonResponse({'success': False, 'message': 'Mauvaise methode de requete.'}, status=400)

def inscriptionprocessus(request):
    if request.method == 'POST':
       ...
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def mdpoublieprocessus(request):
    return 

# Pages standards
@login_required(login_url='connexion')
def AjouterAccident(request):
    return render(request,'Formulaire.html')

@login_required(login_url='connexion')
def tableauAction(request):
    return render(request,'tab_actions.html')

@login_required(login_url='connexion')
def profile(request):
    return render(request,'users-profile.html')


# fonction utilitaires
def existenceID(stringID):
    exists = ID_unique.objects.filter(identifiant=stringID).exists()
    return exists
    
def generateurID_Entreprise():
    while True:
        choix = [str(Generateur.randint(0, 100000000)) for _ in range(2)]
        identifiant = 'DQ.E.' + ''.join(choix)
        if not existenceID(identifiant):
            return identifiant