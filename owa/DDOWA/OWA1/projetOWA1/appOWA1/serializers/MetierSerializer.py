from rest_framework import serializers
from ..models import CV, Metier

class MetierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metier
        fields = ['id', 'nom', 'description']
