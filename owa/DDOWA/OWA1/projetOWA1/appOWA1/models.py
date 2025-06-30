from django.db import models
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model

from projetOWA1 import settings
# Create your models here.
class AppUtilisateurManager(BaseUserManager):
    def create_user(self, username, password=None, nom=None, prenom=None, poste=None, roles=None, **extra_fields):
        if not username:
            raise ValueError('Le nom d’utilisateur est obligatoire')
        if not nom:
            raise ValueError('Le nom est obligatoire')
        if not prenom:
            raise ValueError('Le prénom est obligatoire')
        if not poste:
            raise ValueError('Le poste est obligatoire')

        user = self.model(
            username=username,
            nom=nom,
            prenom=prenom,
            poste=poste,
            **extra_fields
        )
        user.set_password(password)
        user.save()

        # Attribution des rôles ManyToMany après le save
        if roles:
            if all(isinstance(r, str) for r in roles):
                from .models import Role  # Import local pour éviter les imports circulaires
                role_objs = Role.objects.filter(name__in=roles)
            else:
                role_objs = roles
            user.roles.set(role_objs)

        return user

    def create_superuser(self, username, password=None, nom=None, prenom=None, poste=None, roles=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not password:
            raise ValueError('Le mot de passe est obligatoire pour un superuser')

        return self.create_user(
            username=username,
            password=password,
            nom=nom,
            prenom=prenom,
            poste=poste,
            roles=roles,
            **extra_fields
        )
    
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Entreprise(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=150, unique=True)
    adresse_siege = models.CharField(max_length=100)
    image = models.ImageField(upload_to='entreprises_images/', null=True, blank=True)
    entreprise_infos = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.nom

   
class Utilisateur(AbstractBaseUser, PermissionsMixin):
    objects = AppUtilisateurManager()
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email=models.CharField(max_length=120, null=True, blank=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    poste = models.CharField(max_length=100)  

    roles = models.ManyToManyField(Role, related_name='utilisateurs', blank=True, null=True)

    entreprise = models.ForeignKey(
        'Entreprise',
        on_delete=models.CASCADE,
        related_name='utilisateurs',
        null=True,
        blank=True
    )

    is_staff = models.BooleanField(default=False)
    is_active  = models.BooleanField(default=True) 

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nom', 'prenom', 'poste']  # Correction du nom du champ

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='application_users',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='application_users',
        blank=True
    )

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.username})"




class OffresEmploi(models.Model):
    id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True,blank=True)
    metier_propose = models.CharField(max_length=100)
    secteur_activite = models.CharField(max_length=100)
    Experience_requise = models.CharField(max_length=100)
    niveau_etude = models.CharField(max_length=100)
    type_contrat = models.CharField(max_length=100)
    date_publication = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateTimeField()
    profil_recherche = models.TextField(null=True,blank=True)
    entreprise = models.ForeignKey(
        'Entreprise',
        on_delete=models.CASCADE,
        related_name='offres',
        null=True,
        blank=True
    )




class Metier(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=500)


class CV(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(
        Utilisateur,
        related_name="cvs",
        on_delete=models.CASCADE,
        null=True,        # ← temporaire
        blank=True        # ← temporaire
    )

    texte_brut = models.TextField(null=True,blank=True)
    fichier = models.FileField(upload_to="cvs/", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)
    # résultat brut de la classification (classe prédite)
    is_classe = models.BooleanField(default=False)
    formations = models.TextField(null=True,blank=True)
    experiences = models.TextField(null=True,blank=True)
    competences = models.TextField(null=True,blank=True)
    langues = models.TextField(null=True,blank=True)
    permis_conduite = models.TextField(null=True,blank=True)

    metier =  models.ForeignKey(
        Metier,
        related_name="cvs",
        on_delete=models.CASCADE,
        null=True,        # ← temporaire
        blank=True        # ← temporaire
    )

    offres = models.ManyToManyField(OffresEmploi, 
                                    related_name='cvs', 
                                    blank=True, null=True,
                                    through='CV_Offre')

    
    
class CV_classe(models.Model):
    id = models.AutoField(primary_key=True)
    cv = models.ForeignKey(
        CV,
        related_name="cv_classes",
        on_delete=models.CASCADE,
    )
    metiers = models.JSONField()  # Liste des classes avec probabilités
    date = models.DateTimeField(default=timezone.now)



class CV_Offre(models.Model):
    cv = models.ForeignKey('CV', on_delete=models.CASCADE)
    offre = models.ForeignKey('OffresEmploi', on_delete=models.CASCADE)
    selected = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    score= models.FloatField(null=True, blank=True, verbose_name="Score de test")

    class Meta:
        unique_together = ('cv', 'offre')

    def __str__(self):
        return f"CV: {self.cv_id} - Offre: {self.offre_id} (selected={self.selected})"    
    



class Contact(models.Model):
    nom = models.CharField(max_length=120)
    email = models.EmailField()
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} <{self.email}> - {self.sujet}"

