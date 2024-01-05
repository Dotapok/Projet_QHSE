from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http import JsonResponse
from django.contrib.auth.models import User
import random as Generateur
from django.contrib.auth.decorators import login_required
from Acceuil.models import *

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

        user = authenticate(request,email=email, password=pwd)
        if user:
            login(request, user)
            redirection_url = '/Dashboard/'
            return JsonResponse({'success': True,'redirection_url': redirection_url})
        else:
            return JsonResponse({'success': False}, status=401)
    else:
        return JsonResponse({'success': False, 'message': 'Mauvaise methode de requete.'}, status=400)

def inscriptionprocessus(request):
    if request.method == 'POST':
        nom_entreprise = request.POST.get('nomEntreprise')
        description = request.POST.get('description')
        nombre_employe = request.POST.get('nombreEmploye')
        secteur_activite = request.POST.get('secteurActivite')
        adresse = request.POST.get('adresse')
        telephone_entreprise = request.POST.get('telephone')
        email_entreprise = request.POST.get('email')

        nom_admin = request.POST.get('nom')
        fonction_admin = request.POST.get('fonction')
        email_admin = request.POST.get('email')
        telephone_admin = request.POST.get('telephone')
        mot_de_passe_admin = request.POST.get('mdp')

        # Récupérer les fichiers téléchargés
        logo_entreprise = request.FILES.get('logoEntreprise')
        img_profil_admin = request.FILES.get('imgProfil')

        idEnt = generateurID_Entreprise()
        
        compte_entreprise = CompteEntreprise.objects.create(
            id_entreprise=idEnt,
            nomEntreprise=nom_entreprise,
            description=description,
            nombreEmploye=nombre_employe,
            secteurActivite=secteur_activite,
            adresse=adresse,
            telephone=telephone_entreprise,
            email=email_entreprise,
        )

        compte_utilisateur = CompteUtilisateur.objects.create(
            fonction=fonction_admin,
            telephone=telephone_admin,
            typeCompte='admin',
            entrepriseID=compte_entreprise,
            username=email_admin,
            email=email_admin,
            first_name=nom_admin,
        )

        compte_utilisateur.set_password(mot_de_passe_admin)

        
        if logo_entreprise:
            compte_entreprise.logoEntreprise = logo_entreprise
        compte_entreprise.save()

        if img_profil_admin:
            compte_utilisateur.imgProfil = img_profil_admin
        compte_utilisateur.save()
        iduni=ID_unique.objects.create(identifiant=idEnt,type='Entreprise')
        iduni.save()
        
        response_data = {'message': 'Compte entreprise créé avec succès.'}
        return JsonResponse(response_data, status=200)
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