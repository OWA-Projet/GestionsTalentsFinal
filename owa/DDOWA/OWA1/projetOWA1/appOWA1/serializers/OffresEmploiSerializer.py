# serializers/OffresEmploiSerializer.py
from rest_framework import serializers
from ..models import OffresEmploi, Entreprise

class EntrepriseLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entreprise
        fields = ['id', 'nom', 'adresse_siege', 'image']

class OffresEmploiSerializer(serializers.ModelSerializer):
    entreprise = EntrepriseLightSerializer(read_only=True)
    entreprise_id = serializers.PrimaryKeyRelatedField(
        queryset=Entreprise.objects.all(), source='entreprise', write_only=True, required=False
    )

    class Meta:
        model = OffresEmploi
        fields = '__all__'
