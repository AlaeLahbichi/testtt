from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Chef_projet','Chef_projet'),
        ('Collaborateur','Collaborateur'),
        ('Employe_Integration','Employe_Integration'),
        ('Stagiaire','Stagiaire'),
        ('Utilisateur_Confirmé' , 'Utilisateur_Confirmé'),
        ('Utilisateur_Temporaire','Utilisateur_Temporaire'),
    ]
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default='Utilisateur_Temporaire')
    phone_number = models.CharField(max_length=50,blank=True,null=True)
    adress = models.CharField(max_length=100,blank=True,null=True)
    ProfileImage = models.ImageField(upload_to="profileimage/" , default="profileimage/default.png")

class Project(models.Model):
    CAUTION_CHOICES = [
        ('ELECTRONIQUE','ELECTRONIQUE') , 
        ('PHYSIQUE' , 'PHYSIQUE'),
    ]
    ETAT_CHOICES = [
        ('PP' , 'PP') , 
        ('PEC' , 'PEC'),
        ('PA' , 'PA'),
        ('PG' , 'PG'),
    ]
    reference = models.CharField(max_length=100)
    reference_modcod = models.CharField(max_length=100)
    objet = models.TextField()
    date_limite_reponse = models.DateTimeField()
    caution = models.CharField(max_length=100, choices=CAUTION_CHOICES , default="ELECTRONIQUE")
    delai_execution = models.DateField(blank=True, null=True)
    prospectus = models.DateField(blank=True, null=True)
    editeur = models.CharField(max_length=100, blank=True, null=True)
    contexte = models.CharField(max_length=100, blank=True, null=True)
    documents_manquants = models.TextField(blank=True, null=True)
    etat_d_avancement = models.CharField(max_length=255,blank=True, null=True)
    etape_suivante = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255,choices=ETAT_CHOICES,default='PA',blank=True,null=True)
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.reference_modcod} - {self.reference}"

class Reclamation(models.Model):
    CATEGORIE_RECLAMATION_CHOICES = [
    ('Bug technique', 'Bug technique'),
    ('Erreur de données', 'Erreur de données'),
    ('Problème d\'affichage', 'Problème d\'affichage'),
    ('Fonctionnalité manquante', 'Fonctionnalité manquante'),
    ('Performance lente', 'Performance lente'),
    ('Problème de collaboration', 'Problème de collaboration'),
    ('Problème de fichiers / téléchargements', 'Problème de fichiers / téléchargements'),
    ('Erreurs de permissions', 'Erreurs de permissions'),
    ('Sécurité / Confidentialité', 'Sécurité / Confidentialité'),
    ('Problème d\'accès / Authentification', 'Problème d\'accès / Authentification'),
    ('Autre', 'Autre'),
    ]
    STATUS_CHOICES = [
    ('En attente', 'En attente'),
    ('En cours', 'En cours'),
    ('Résolu', 'Résolu'),
    ('Non résolu', 'Non résolu'),
    ]
    Priorité_Choices = [
        ('Faible','Faible'),
        ('Moyen','Moyen'),
        ('Urgent','Urgent'),
        ('Not defined' , 'Not defined')
    ]
    username = models.CharField(max_length=50,default="")
    email = models.EmailField(max_length=200,default="")
    référence = models.CharField(max_length=150,blank=True,null=True)
    catégorie = models.CharField(max_length=255,choices=CATEGORIE_RECLAMATION_CHOICES,default="Autre")
    priorité = models.CharField(max_length=100,choices=Priorité_Choices,default="Not defined")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='En attente')
    sujet = models.CharField(max_length=500,default="")
    description = models.TextField(max_length=2000,default="")
    piece = models.FileField(upload_to='uploads/', blank=True, null=True)
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Réclamation numéro {self.id}"
    
class Logs(models.Model):
    Action_Choices = [
        ('Create' , 'Create') , 
        ('Update' , 'Update') ,
        ('Delete' , 'Delete'),
        ('Not defined' , 'Not defined')
    ]
    user = models.ForeignKey( CustomUser , on_delete=models.CASCADE )
    action = models.CharField(max_length=100,choices=Action_Choices , default="Not defined")
    description = models.CharField(max_length=1000,blank=True,null=True)
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"LOG-{self.id}"
