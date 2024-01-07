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
    
    objects = CompteUtilisateurManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def get_username(self):
        return self.email
    
    def __str__(self):
        return self.email