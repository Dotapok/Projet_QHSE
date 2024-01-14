from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login,logout
from django.http import JsonResponse
from django.core.mail import send_mail
import random as Generateur
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import get_user_model
from datetime import date
from django.core.serializers import serialize

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
    date_actuelle = date.today()

    nombreAccidentAvecArret = Accident.objects.filter(
        decisionFinale='Avec arret de travail').count()
    nombreAccidentSansArret = Accident.objects.filter(
        decisionFinale='Sans arrêt de travail').count()
    nombreAccidentIncident = Accident.objects.filter(
        typeEvenement='Incidents').count()
    nombreAccidentPresqueIncident = Accident.objects.filter(
        typeEvenement="Presqu'incidents").count()

    plan_actions_en_retard = PlanAction.objects.filter(
        date_fin__lt=date_actuelle)

    nombreActionEnCours = PlanAction.objects.filter(statut='En cours').count()
    nombreActionOuvert = PlanAction.objects.filter(statut='Ouvert').count()
    nombreActionTermine = PlanAction.objects.filter(statut='Terminé').count()
    nombreActionsRetard = PlanAction.objects.filter(
        date_fin__lt=date_actuelle).count()

    context = {
        'entreprise_nom': request.session['entreprise'],
        'nom': request.session['nom'],
        'email': request.session['email'],
        'fonction': request.session['fonction'],
        'telephone': request.session['telephone'],
        'type_compte': request.session['typeCompte'],
        'profile_image_url': request.session['image_profile'],
        
        'nombreAccidentAvecArret': nombreAccidentAvecArret,
        'nombreAccidentSansArret': nombreAccidentSansArret,
        'nombreAccidentIncident': nombreAccidentIncident,
        'nombreAccidentPresqueIncident': nombreAccidentPresqueIncident,

        'nombreActionEnCours': nombreActionEnCours,
        'nombreActionOuvert': nombreActionOuvert,
        'nombreActionTermine': nombreActionTermine,
        'nombreActionsRetard': nombreActionsRetard,
    }
    return render(request,'dashboard.html',context)

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
    context = {
        'entreprise_nom': request.session['entreprise'],
        'nom': request.session['nom'],
        'email': request.session['email'],
        'fonction': request.session['fonction'],
        'telephone': request.session['telephone'],
        'type_compte': request.session['typeCompte'],
        'profile_image_url': request.session['image_profile'],
    }
    return render(request,'Formulaire.html',context)

@login_required(login_url='connexion')
def AjouterIncident(request):
    context = {
        'entreprise_nom': request.session['entreprise'],
        'nom': request.session['nom'],
        'email': request.session['email'],
        'fonction': request.session['fonction'],
        'telephone': request.session['telephone'],
        'type_compte': request.session['typeCompte'],
        'profile_image_url': request.session['image_profile'],
    }
    return render(request,'Formulaire_incident.html',context)

@login_required(login_url='connexion')
def tableauAccident(request):
    context = {
        'entreprise_nom': request.session['entreprise'],
        'nom': request.session['nom'],
        'email': request.session['email'],
        'fonction': request.session['fonction'],
        'telephone': request.session['telephone'],
        'type_compte': request.session['typeCompte'],
        'profile_image_url': request.session['image_profile'],
    }
    return render(request,'tab_accidents.html',context)

@login_required(login_url='connexion')
def tableauAction(request):
    context = {
        'entreprise_nom': request.session['entreprise'],
        'nom': request.session['nom'],
        'email': request.session['email'],
        'fonction': request.session['fonction'],
        'telephone': request.session['telephone'],
        'type_compte': request.session['typeCompte'],
        'profile_image_url': request.session['image_profile'],
    }
    return render(request,'tab_actions.html',context)

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


# fonctions asynchrones
# dashboard
def initialisation(request):
    return 

# profile
def listeUsers(request):
    return

def updateProfil(request):
    return

def updatePass(request):
    return

def addUser(request):
    return

# accident
def AjouterAccidentProcessus(request):
    return

def tableauAccidentListe(request):
    accidents = Accident.objects.all()
    serialized_accidents = serialize('json', accidents)
    return JsonResponse({'accidentData': serialized_accidents}, safe=False)

# incident
def AjouterIncidentProcessus(request):
    if request.method == 'POST':
        eventType = request.POST.get('eventType')
        eventTitle = request.POST.get('eventTitle')
        accidentDate = request.POST.get('accidentDate')
        accidentTime = request.POST.get('accidentTime')
        accidentLocation = request.POST.get('accidentLocation')
        nameOrCorporateName = request.POST.get('nameOrCorporateName')
        natureOfLesions = request.POST.get('natureOfLesions')
        locationOfLesions = request.POST.get('locationOfLesions')
        detailedCircumstances = request.POST.get('detailedCircumstances')
        dropdownData = request.POST.getlist('dropdownData')
        
        print(eventType)

        # # Récupérer les données du troisième onglet du formulaire
        # # Vous devrez ajuster le code en fonction de la structure exacte de votre tableau
        # actionsData = []
        # for i in range(1, int(request.POST.get('totalActions', 0)) + 1):
        #     actionData = {
        #         'title': request.POST.get(f'actionTitle_{i}'),
        #         'description': request.POST.get(f'actionDescription_{i}'),
        #         'responsible': request.POST.get(f'actionResponsible_{i}'),
        #         'status': request.POST.get(f'actionStatus_{i}'),
        #         'startDate': request.POST.get(f'actionStartDate_{i}'),
        #         'endDate': request.POST.get(f'actionEndDate_{i}'),
        #     }
        #     actionsData.append(actionData)

        # # Enregistrez les données dans votre modèle
        # try:
        #     # Remplacez VotreModele par le nom de votre modèle
        #     incident = VotreModele.objects.create(
        #         eventType=eventType,
        #         eventTitle=eventTitle,
        #         accidentDate=accidentDate,
        #         accidentTime=accidentTime,
        #         accidentLocation=accidentLocation,
        #         nameOrCorporateName=nameOrCorporateName,
        #         natureOfLesions=natureOfLesions,
        #         locationOfLesions=locationOfLesions,
        #         detailedCircumstances=detailedCircumstances,
        #     )

        #     # Enregistrez les données associées dans votre modèle lié (si applicable)
        #     # Par exemple, si vous avez une clé étrangère vers un autre modèle,
        #     # vous pouvez l'ajuster en conséquence.

        #     # Enregistrez les données du deuxième onglet (drop-down) dans votre modèle lié (si applicable)

        #     # Enregistrez les données du troisième onglet (tableau d'actions) dans votre modèle lié (si applicable)
        #     for actionData in actionsData:
        #         incident.actions_set.create(**actionData)

        #     messages.success(request, 'Incident ajouté avec succès!')
        #     return redirect('votre_url_de_redirection')  # Remplacez par la route souhaitée
        # except Exception as e:
        #     messages.error(request, f'Erreur lors de l\'ajout de l\'incident: {e}')

    # Gérer le cas où la méthode HTTP n'est pas POST
    # ...

    return render(request, 'votre_template.html')


def tableauActionListe(request):
    actionsAccident = PlanAction.objects.all()
    serialized_actionsAccident = serialize('json', actionsAccident)
    return JsonResponse({'actionsData': serialized_actionsAccident}, safe=False)

