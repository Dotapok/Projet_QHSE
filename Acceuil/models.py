from django.db import models
from django.contrib.auth.models import AbstractUser

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
    
class CompteUtilisateur(AbstractUser):
    imgProfil = models.ImageField(upload_to='profiles/',blank=True)
    fonction = models.CharField(max_length=250)
    telephone = models.CharField(max_length=100)
    typeCompte = models.CharField(max_length=10,choices=[('admin','Admin'),('user','User'),('manager','Manager')])
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