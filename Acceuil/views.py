import json
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
    nombreAccidentIncident = nombreAccidentIncident + Incident.objects.count()
    nombreAccidentPresqueIncident = Accident.objects.filter(
        typeEvenement="Presqu'incidents").count()

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
            entreprise_IDBD = user.entrepriseID.id if user.entrepriseID else None
            
            login(request, user)
            request.session['entreprise'] = entreprise_nom
            request.session['nom'] = user.first_name
            request.session['email'] = user.email
            request.session['fonction'] = user.fonction
            request.session['telephone'] = user.telephone
            request.session['typeCompte'] = user.typeCompte
            request.session['entrepriseID'] = entreprise_id
            request.session['entrepriseIDBD'] = entreprise_IDBD
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

def generateurID_Incident():
    while True:
        choix = [str(Generateur.randint(0, 100000000)) for _ in range(2)]
        identifiant = 'DQ.I.' + ''.join(choix)
        if not existenceID(identifiant):
            return identifiant
        
def generateurID_ActionIncident():
    while True:
        choix = [str(Generateur.randint(0, 100000000)) for _ in range(2)]
        identifiant = 'DQ.ACI.' + ''.join(choix)
        if not existenceID(identifiant):
            return identifiant

def generateurID_Accident():
    while True:
        choix = [str(Generateur.randint(0, 100000000)) for _ in range(2)]
        identifiant = 'DQ.AC.' + ''.join(choix)
        if not existenceID(identifiant):
            return identifiant
        
def generateurID_Victime():
    while True:
        choix = [str(Generateur.randint(0, 100000000)) for _ in range(2)]
        identifiant = 'DQ.V.' + ''.join(choix)
        if not existenceID(identifiant):
            return identifiant
        
def generateurID_CauseAccident():
    while True:
        choix = [str(Generateur.randint(0, 100000000)) for _ in range(2)]
        identifiant = 'DQ.CA.' + ''.join(choix)
        if not existenceID(identifiant):
            return identifiant
        
def generateurID_ActionAccident():
    while True:
        choix = [str(Generateur.randint(0, 100000000)) for _ in range(2)]
        identifiant = 'DQ.AA.' + ''.join(choix)
        if not existenceID(identifiant):
            return identifiant
        
def generateurID_Temoin():
    while True:
        choix = [str(Generateur.randint(0, 100000000)) for _ in range(2)]
        identifiant = 'DQ.T.' + ''.join(choix)
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
def updateProfil(request):
    return

def updatePass(request):
    return

def addUser(request):
    # Récupérer les données du formulaire depuis la requête POST
    nom_user = request.POST.get('name')
    fonction_user = request.POST.get('fonction')
    email_user = request.POST.get('email')
    telephone_user = request.POST.get('phone')
    mot_de_passe_user = request.POST.get('password')
    img_profil_user = request.FILES.get('image')
    typeCompte = request.POST.get('compte')
    entreprise = CompteEntreprise.objects.get(id=request.session['entrepriseIDBD'])

    try:
        compte_utilisateur = CompteUtilisateur.objects.create(
            fonction=fonction_user,
            telephone=telephone_user,
            typeCompte=typeCompte,
            entrepriseID=entreprise,
            email=email_user,
            first_name=nom_user,
        )
        compte_utilisateur.set_password(mot_de_passe_user)

        if img_profil_user:
            compte_utilisateur.imgProfil = img_profil_user
        compte_utilisateur.save()
        
        
        
        utilisateurs = CompteUtilisateur.objects.filter(entrepriseID=request.session['entrepriseIDBD'])
        serialized_utilisateurs = serialize('json', utilisateurs)
        response_data = {'message': 'Utilisateur enregistré avec succès!','utilisateurs':serialized_utilisateurs}
        return JsonResponse(response_data, safe=False)
    except:
        utilisateurs = CompteUtilisateur.objects.filter(entrepriseID=request.session['entrepriseIDBD'])
        serialized_utilisateurs = serialize('json', utilisateurs)
        response_data = {'message': "Impossible d'enregistrer cet utilisateur.",'utilisateurs':serialized_utilisateurs}
        return JsonResponse(response_data, safe=False)

def Users(request):
    utilisateurs = CompteUtilisateur.objects.filter(entrepriseID=request.session['entrepriseIDBD'])
    serialized_utilisateurs = serialize('json', utilisateurs)
    return JsonResponse({'utilisateurs': serialized_utilisateurs}, safe=False)

# accident
def AjouterAccidentProcessus(request):
    if request.method == 'POST':
        numberCotisant = request.POST.get('numberCotisant')
        nameOrCorporateName = request.POST.get('nameOrCorporateName')
        acronym = request.POST.get('acronym')
        address = request.POST.get('address')
        phoneNumber = request.POST.get('phoneNumber')
        fax = request.POST.get('fax')
        email = request.POST.get('email')
        activitySector = request.POST.get('activitySector')
        numberOfEmployees = request.POST.get('numberOfEmployees')
        eventTitle = request.POST.get('eventTitle')
        accidentDate = request.POST.get('accidentDate')
        accidentTime = request.POST.get('accidentTime')
        
        eventType = request.POST.get('eventType')
        accidentLocation = request.POST.get('accidentLocation')
        workSchedule = request.POST.get('workSchedule')
        natureOfLesions = request.POST.get('natureOfLesions')
        locationOfLesions = request.POST.get('locationOfLesions')
        firstAidProvider = request.POST.get('firstAidProvider')
        detailedCircumstances = request.POST.get('detailedCircumstances')

        #causeOfAccident = request.POST.get('causeOfAccident')
        probableOutcome = request.POST.get('probableOutcome')
        workStoppage = request.POST.get('workStoppage')
        #stoppageDays = request.POST.get('stoppageDays')

        socialSecurityNumber = request.POST.get('socialSecurityNumber')
        fullNameV = request.POST.get('fullNameV')
        genderV = request.POST.get('genderV')
        addressV = request.POST.get('addressV')
        phoneNumberV = request.POST.get('phoneNumberV')
        faxV = request.POST.get('faxV')
        emailV = request.POST.get('emailV')
        hiringDate = request.POST.get('hiringDate')
        nationality = request.POST.get('nationality')
        profession = request.POST.get('profession')
        jobPosition = request.POST.get('jobPosition')
        seniority = request.POST.get('seniority')
        spouseFullName = request.POST.get('spouseFullName')
        spousePhoneNumber = request.POST.get('spousePhoneNumber')

        witnessName = request.POST.get('witnessName')
        witnessAddress = request.POST.get('witnessAddress')
        policeReport = request.POST.get('policeReport')
        reportAuthor = request.POST.get('reportAuthor')

        riskName = request.POST.get('riskName')
        riskAddress = request.POST.get('riskAddress')
        insuranceCompany = request.POST.get('insuranceCompany')
        thirdParty = request.POST.get('thirdParty')
        policyNumber = request.POST.get('policyNumber')

        try:
            idAC = generateurID_Accident()
            idVic = generateurID_Victime()
            idTem = generateurID_Temoin()

            accident_instance = Accident(
                identifiant_uniqueAccident=idAC,
                NumCotisant=numberCotisant,
                raisonSociale=nameOrCorporateName,
                sigle=acronym,
                adresse=address,
                numtel=phoneNumber,
                fax=fax,
                email=email,
                secteurActivite=activitySector,
                nombreSalarie=numberOfEmployees,
                titreEvenement=eventTitle,
                date_accident=accidentDate,
                heure_accident=accidentTime,
                typeEvenement=eventType,
                lieu=accidentLocation,
                circonstances=detailedCircumstances,
                horaireTravail=workSchedule,
                natureLesions=natureOfLesions,
                siegeLesion=locationOfLesions,
                NomMedecin=firstAidProvider,
                suiteProbable=probableOutcome,
                decisionFinale=workStoppage,
                declarant=request.session['email'],
            )
            
            accident_instance.save()
            iduni=ID_unique.objects.create(identifiant=idAC,type='Accident')
            iduni.save()

            victime_instance = Victime(
                identifiant_uniqueVictime=idVic,
                id_accident=accident_instance,  # Utilisez l'instance d'accident que vous avez créée
                numeroAssurance=socialSecurityNumber,
                nom_victime=fullNameV,
                sexe=genderV,
                adresse=addressV,
                numeroTel=phoneNumberV,
                fax=faxV,
                email=emailV,
                dateEmbauche=hiringDate,
                nationalite=nationality,
                profession=profession,
                posteTravail=jobPosition,
                ancienetePoste=seniority,
                nomPrenomProche=spouseFullName,
                numTelephone=spousePhoneNumber,
            )
            
            victime_instance.save()
            iduni=ID_unique.objects.create(identifiant=idVic,type='Victime')
            iduni.save()

            temoin_instance = Temoin(
                identifiant_uniqueTemoin=idTem,
                id_accident=accident_instance,
                nomPrenom_temoin=witnessName,
                adresseTemoin=witnessAddress,
                rapportPolice=policeReport,
                ParQui=reportAuthor,
                nomTiers=riskName,
                adresseTiers=riskAddress, 
                cleAssuranceTiers=insuranceCompany, 
                duTiers=thirdParty, 
                numPoliceTiersAssurance=policyNumber,
            )
            
            temoin_instance.save()
            iduni=ID_unique.objects.create(identifiant=idTem,type='Temoin')
            iduni.save()
            
            selected_causes = request.POST.getlist('causes[]')
            
            for cause_label in selected_causes:
                idCause = generateurID_CauseAccident()
                cause_instance = Cause.objects.create(identifiant_uniqueCause=idCause,id_accident=accident_instance,causeLibele=cause_label)
                iduniCause = ID_unique.objects.create(identifiant=idCause, type='Cause Accident')
            print('ici')

            actions_data = request.POST.get('actionsAccidents')
            
            for action_data in json.loads(actions_data):
                idACAcc = generateurID_ActionAccident()
                action_instance = PlanAction.objects.create(
                    id_accident=accident_instance,
                    titreAction=action_data['title'],
                    description=action_data['description'],
                    responsable=action_data['responsible'],
                    date_debut=action_data['startDate'],
                    date_fin=action_data['endDate'],
                    statut=action_data['status'],
                )
                iduniActAccident = ID_unique.objects.create(identifiant=idACAcc, type='Action Accident')
            print('ici')
            PlanAction.objects.bulk_create(cause_instance)
            ID_unique.objects.bulk_create(iduniCause)
            PlanAction.objects.bulk_create(action_instance)
            ID_unique.objects.bulk_create(iduniActAccident)

            response_data = {'message': 'Accident enregistré avec succès.'}
            return JsonResponse(response_data, status=200) 
        except:
            response_data = {'error': "Impossible d'enregistrer cet accident"}
            return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def tableauAccidentListe(request):
    accidents = Accident.objects.prefetch_related('accident_Victime').values(
        'id', 'titreEvenement', 'date_accident', 'typeEvenement', 'lieu', 'accident_Victime__nom_victime'
    )
    return JsonResponse({'accidentData': list(accidents)}, safe=False)

# incident
def AjouterIncidentProcessus(request):
    if request.method == 'POST':
        eventType = request.POST.get('eventType')
        eventTitle = request.POST.get('eventTitle')
        accidentDate = request.POST.get('accidentDate')
        accidentTime = request.POST.get('accidentTime')
        accidentLocation = request.POST.get('accidentLocation')
        natureOfLesions = request.POST.get('natureOfLesions')
        locationOfLesions = request.POST.get('locationOfLesions')
        detailedCircumstances = request.POST.get('detailedCircumstances')
        informationActions = json.loads(request.POST.get('informationActions'))
        
        try:
            idInc = generateurID_Incident()
            incident = Incident.objects.create(
                identifiant_uniqueIncident=idInc,
                typeEvenement=eventType,
                titreEvenement=eventTitle,
                date_Incident=accidentDate,
                heure_Incident=accidentTime,
                lieuIncident=accidentLocation,
                natureLesion=natureOfLesions,
                siegeLesion=locationOfLesions,
                actionImediate=detailedCircumstances,
                declarant=request.session['email'])

            for action_data in informationActions:
                idACInc = generateurID_ActionIncident()
                actions = PlanActionIncident.objects.create(
                    identifiant_uniqueAction=idACInc,
                    id_incident=incident,
                    titreAction=action_data.get('title'),
                    description=action_data.get('description'),
                    responsable=action_data.get('responsible'),
                    date_debut=action_data.get('startDate'),
                    date_fin=action_data.get('endDate'),
                    statut=action_data.get('status'),
                )
                iduniAct=ID_unique.objects.create(identifiant=idACInc,type='Action Incident')
                
            incident.save()
            PlanActionIncident.objects.bulk_create(actions)
            ID_unique.objects.bulk_create(iduniAct)
            iduni=ID_unique.objects.create(identifiant=idInc,type='Incident')
            iduni.save()
            response_data = {'message': 'Incident enregistré avec succès.'}
            return JsonResponse(response_data, status=200) 
        except:
            response_data = {'error': "Impossible d'enregistrer cet incident"}
            return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


def tableauActionListe(request):
    actionsAccident = PlanAction.objects.all()
    serialized_actionsAccident = serialize('json', actionsAccident)
    return JsonResponse({'actionsData': serialized_actionsAccident}, safe=False)

