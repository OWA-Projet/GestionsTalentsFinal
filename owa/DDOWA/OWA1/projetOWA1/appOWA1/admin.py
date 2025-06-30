from django.contrib import admin

from .models import CV, CV_classe, Utilisateur, Role,Metier,Entreprise,CV_Offre,OffresEmploi


# Register your models here.

admin.site.register(Utilisateur)
admin.site.register(CV)
admin.site.register(CV_classe)
admin.site.register(Role)
admin.site.register(Metier)
admin.site.register(Entreprise)
admin.site.register(CV_Offre)
admin.site.register(OffresEmploi)
