"""
URL configuration for projetOWA1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from appOWA1.views.MeView import MeView
from appOWA1.views.EntrepriseSetView import EntrepriseViewSet
from appOWA1.views.RegisterAPIView import RegisterView
from appOWA1.views.LoginAPIView import LoginAPIView
from appOWA1.views.LogoutAPIView import LogoutAPIView
from appOWA1.views.CVviewSet import CVViewSet
from appOWA1.views.CVviewSetForCandidat import CVviewSetForCandidat
from appOWA1.views.OffresEmploiViewSet import OffresEmploiViewSet
from rest_framework.routers import DefaultRouter
from appOWA1.views.OffresAcceuil import OffresAcceuilViewSet
from appOWA1.views.PostulerOffreAPIView import PostulerOffreAPIView
from appOWA1.views.MetierViewSet import MetierViewSet  # ou adapte selon emplacement
from appOWA1.views.UserViewSet import UserViewSet
from appOWA1.views.ContactAPIView import ContactAPIView


router = DefaultRouter()
router.register(r"api/cvs", CVViewSet, basename="cv")
router.register(r"api/cvs_candidat",CVviewSetForCandidat, basename="cv_candidat")
router.register(r"api/offres-emploi", OffresEmploiViewSet, basename="offres-emploi")
router.register(r"api/offres-acceuil",OffresAcceuilViewSet, basename="offres-acceuil")
router.register(r'api/entreprises', EntrepriseViewSet, basename='entreprise')
router.register(r'api/metiers', MetierViewSet, basename='metier')
router.register(r'api/utilisateurs', UserViewSet, basename='utilisateur')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/logout/',LogoutAPIView.as_view(),name='logout'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/Postuler/',PostulerOffreAPIView.as_view(), name='postuler'),
    path('api/contact/', ContactAPIView.as_view(), name='contact-api'),
    path('api/me/', MeView.as_view()),

    path('',include(router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
