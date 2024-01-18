from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin,BaseUserManager
from django.utils.translation import gettext_lazy as _


# Create your models here.
class ID_unique(models.Model):
    identifiant = models.CharField(max_length=150,unique=True)
    type = models.CharField(max_length=150)

class CompteEntreprise(models.Model):
    id_entreprise = models.CharField(max_length=100,unique=True)
    nomEntreprise = models.CharField(max_length=250, unique=True)
    logoEntreprise = models.ImageField(upload_to='logos/',blank=True)                                                                                
    description = models.TextField()
    nombreEmploye = models.IntegerField()
    secteurActivite = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)
    telephone = models.CharField(max_length=50)
    email = models.EmailField()
    dateCreationCompte = models.DateTimeField(auto_now_add=True)
    
class CompteUtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CompteUtilisateur(AbstractUser,PermissionsMixin):
    username=None
    email = models.EmailField(_("email address"), unique=True)
    imgProfil = models.ImageField(upload_to='profiles/',blank=True)
    fonction = models.CharField(max_length=250)
    telephone = models.CharField(max_length=100)
    typeCompte = models.CharField(max_length=10,choices=[('admin','Admin'),('user','Utilisateur'),('manager','Manager')])
    entrepriseID = models.ForeignKey(CompteEntreprise, on_delete=models.CASCADE, related_name='entreprise_utilisateurs')
    dateCreationCompte = models.DateTimeField(auto_now_add=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='compte_utilisateurs_groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='compte_utilisateurs_permissions'
    )
    
    objects = CompteUtilisateurManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def get_username(self):
        return self.email
    
    def __str__(self):
        return self.email


class Accident(models.Model):
    identifiant_uniqueAccident = models.CharField(max_length=50, unique=True)
    NumCotisant = models.CharField(max_length=100)
    raisonSociale = models.CharField(max_length=100)
    sigle = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)
    numtel = models.CharField(max_length=100)
    fax = models.CharField(max_length=100)
    email = models.EmailField()
    secteurActivite = models.CharField(max_length=100)
    nombreSalarie = models.IntegerField()
    titreEvenement = models.CharField(max_length=100)
    date_accident = models.DateField()
    heure_accident = models.TimeField()
    typeEvenement = models.CharField(max_length=100)
    lieu = models.CharField(max_length=100)
    circonstances = models.TextField()
    horaireTravail = models.CharField(max_length=100)
    natureLesions = models.CharField(max_length=100)
    siegeLesion = models.CharField(max_length=100)
    NomMedecin = models.CharField(max_length=100)
    suiteProbable = models.CharField(max_length=100)
    decisionFinale = models.CharField(max_length=100)
    declarant = models.CharField(max_length=100)
    heure_enregistrement_et_jour = models.DateTimeField(auto_now_add=True)
    
class Incident(models.Model):
    identifiant_uniqueIncident = models.CharField(max_length=50, unique=True)
    typeEvenement = models.CharField(max_length=100)
    titreEvenement = models.CharField(max_length=100)
    date_Incident = models.DateField()
    heure_Incident = models.TimeField()
    lieuIncident = models.CharField(max_length=100)
    natureLesion = models.CharField(max_length=100)
    siegeLesion = models.CharField(max_length=100)
    actionImediate = models.CharField(max_length=100)
    declarant = models.CharField(max_length=100)
    heure_enregistrement_et_jour = models.DateTimeField(auto_now_add=True)

# Victimes
class Victime(models.Model):
    identifiant_uniqueVictime = models.CharField(max_length=50, unique=True)
    id_accident = models.ForeignKey(Accident,on_delete=models.CASCADE, related_name='accident_Victime')
    numeroAssurance = models.CharField(max_length=100)
    nom_victime = models.CharField(max_length=250)
    sexe = models.CharField(max_length=20)
    adresse = models.CharField(max_length=250)
    numeroTel = models.CharField(max_length=250)
    fax = models.CharField(max_length=250)
    email = models.EmailField()
    dateEmbauche = models.DateField()
    nationalite = models.CharField(max_length=250)
    profession = models.CharField(max_length=250)
    posteTravail = models.CharField(max_length=250)
    ancienetePoste = models.CharField(max_length=250)
    nomPrenomProche = models.CharField(max_length=250)
    numTelephone = models.CharField(max_length=250)
    
# Temoin et tiers
class Temoin(models.Model):
    identifiant_uniqueTemoignage = models.CharField(max_length=50, unique=True)
    id_accident = models.ForeignKey(Accident, on_delete=models.CASCADE, related_name='accident_Temoignage')
    nomPrenom_temoin = models.CharField(max_length=250)
    adresseTemoin = models.CharField(max_length=250)
    rapportPolice = models.CharField(max_length=20, choices=[('non', 'Non'), (
        'oui', 'Oui')], default='non')
    ParQui = models.CharField(max_length=250,blank=True,null=True)
    nomTiers = models.CharField(max_length=250,blank=True,null=True)
    adresseTiers = models.CharField(max_length=250,blank=True,null=True)
    cleAssuranceTiers = models.CharField(max_length=250,blank=True,null=True)
    duTiers = models.CharField(max_length=250,blank=True,null=True)
    numPoliceTiersAssurance = models.CharField(max_length=250,blank=True,null=True)
    
# Causes
class Cause(models.Model):
    identifiant_uniqueAnalyse = models.CharField(max_length=50, unique=True)
    id_accident = models.ForeignKey(Accident, on_delete=models.CASCADE, related_name='accident_Cause')
    causeLibele = models.CharField(max_length=100)
    
# Actions
class PlanAction(models.Model):
    identifiant_uniqueAction = models.CharField(max_length=50, unique=True)
    id_accident = models.ForeignKey(
        Accident, on_delete=models.CASCADE, related_name='accident_PlanAction')
    titreAction = models.CharField(max_length=250)
    description = models.TextField()
    responsable = models.CharField(max_length=250)
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=20, choices=[(
        'ouvert', 'Ouvert'), ('en cours', 'En cours'), ('termine', 'Terminé')], default='encours')

# Plan d'action inciident
class PlanActionIncident(models.Model):
    identifiant_uniqueAction = models.CharField(max_length=50, unique=True)
    id_incident = models.ForeignKey(
        Incident, on_delete=models.CASCADE, related_name='incident_PlanActionIncident')
    titreAction = models.CharField(max_length=250)
    description = models.TextField()
    responsable = models.CharField(max_length=250)
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=20, choices=[(
        'ouvert', 'Ouvert'), ('encours', 'En cours'), ('termine', 'Terminé')], default='encours')
