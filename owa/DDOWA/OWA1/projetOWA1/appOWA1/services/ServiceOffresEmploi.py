# services/ServiceOffresEmploi.py
from ..models import OffresEmploi
from django.shortcuts import get_object_or_404

class ServiceOffresEmploi:

    @staticmethod
    def list_all(id_entreprise=None):
        queryset = OffresEmploi.objects.all().order_by('-date_publication')
        if id_entreprise is not None:
         queryset = queryset.filter(entreprise__id=id_entreprise)
        return queryset

    @staticmethod
    def retrieve(emploi_id):
        return get_object_or_404(OffresEmploi, id=emploi_id)

    @staticmethod
    def create(validated_data):
        """
        Prend en charge les champs de fichiers (image) si présent dans validated_data.
        """
        # DRF ou Django classique : image déjà prise en compte dans validated_data
        return OffresEmploi.objects.create(**validated_data)

    @staticmethod
    def update(emploi_instance, validated_data):
        """
        Mets à jour chaque champ sauf 'id' et 'date_publication' (lecture seule).
        """
        exclude_fields = ['id', 'date_publication']
        for attr, value in validated_data.items():
            if attr not in exclude_fields:
                setattr(emploi_instance, attr, value)
        emploi_instance.save()
        return emploi_instance

    @staticmethod
    def delete(emploi_instance):
        emploi_instance.delete()
