# services/ServiceEntreprise.py

from ..models import Entreprise
from django.shortcuts import get_object_or_404

class ServiceEntreprise:

    @staticmethod
    def list_all():
        """Retourne toutes les entreprises triées par nom."""
        return Entreprise.objects.all().order_by('nom')

    @staticmethod
    def retrieve(entreprise_id):
        """Récupère une entreprise par ID ou 404."""
        return get_object_or_404(Entreprise, id=entreprise_id)

    @staticmethod
    def create(validated_data):
        """Crée une nouvelle entreprise."""
        return Entreprise.objects.create(**validated_data)

    @staticmethod
    def update(entreprise_instance, validated_data):
        """Met à jour les champs de l'entreprise."""
        for attr, value in validated_data.items():
            setattr(entreprise_instance, attr, value)
        entreprise_instance.save()
        return entreprise_instance

    @staticmethod
    def delete(entreprise_instance):
        """Supprime une entreprise."""
        entreprise_instance.delete()
