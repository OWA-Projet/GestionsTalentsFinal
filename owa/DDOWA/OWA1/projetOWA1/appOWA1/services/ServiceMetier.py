# services/service_metier.py
from ..models import Metier
from django.shortcuts import get_object_or_404

class ServiceMetier:

    @staticmethod
    def list_all():
        return Metier.objects.all()

    @staticmethod
    def retrieve(metier_id):
        return get_object_or_404(Metier, id=metier_id)

    @staticmethod
    def create(validated_data):
        return Metier.objects.create(**validated_data)

    @staticmethod
    def update(metier_instance, validated_data):
        for attr, value in validated_data.items():
            setattr(metier_instance, attr, value)
        metier_instance.save()
        return metier_instance

    @staticmethod
    def delete(metier_instance):
        metier_instance.delete()
