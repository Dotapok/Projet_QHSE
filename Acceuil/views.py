from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login,logout
from django.http import JsonResponse
from django.core.mail import send_mail
import random as Generateur
from django.contrib.auth.decorators import login_required
from Acceuil.models import *
from django.contrib.auth import get_user_model

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
        
        try:
            user = authenticate(request,email=email, password=pwd)
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return JsonResponse({'success': False, 'message': "Compte inexistant"}, status=400)
        
        if user:
            entreprise_id = user.entrepriseID.id_entreprise if user.entrepriseID else None
            entreprise_nom = user.entrepriseID.nomEntreprise if user.entrepriseID else None
            login(request, user)
            request.session['entreprise'] = entreprise_nom
            request.session['nom'] = user.first_name
            request.session['email'] = user.email
            request.session['fonction'] = user.fonction
            request.session['telephone'] = user.telephone
            request.session['typeCompte'] = user.typeCompte
            request.session['entrepriseID'] = entreprise_id
            image_profile_url = f"/media/{user.imgProfil}" if user.imgProfil else None

            # Enregistrez les informations dans la session
            request.session['image_profile'] = image_profile_url

            redirection_url = '/Dashboard/'
            return JsonResponse({'success': True,'redirection_url': redirection_url})
        else:
            return JsonResponse({'success': False,'message':"Erreur lors de la connexion."}, status=401)
    else:
        return JsonResponse({'success': False, 'message': 'Mauvaise methode de requete.'}, status=400)

def deconnexionprocessus(request):
    logout(request)
    redirection_url = '/connexion/'
    return redirect(redirection_url)

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
def AjouterIncident(request):
    return render(request,'Formulaire_incident.html')

@login_required(login_url='connexion')
def tableauAccident(request):
    return render(request,'tab_accidents.html')

@login_required(login_url='connexion')
def tableauAction(request):
    return render(request,'tab_actions.html')

@login_required(login_url='connexion')
def profile(request):
    context = {
        'entreprise_nom': request.session['entreprise'],
        'nom': request.session['nom'],
        'email': request.session['email'],
        'fonction': request.session['fonction'],
        'telephone': request.session['telephone'],
        'type_compte': request.session['typeCompte'],
        'profile_image_url': request.session['image_profile'],
    }
    return render(request,'users-profile.html',context)


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
        
def contacter(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        name = request.POST.get('name')
        
        send_mail(name,message,'settings.EMAIL_HOST_USER',[email],fail_silently=False)
    return render(request,'index.html')