from rest_framework import serializers
from ..models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'nom', 'email', 'sujet', 'message', 'date_envoi']
        read_only_fields = ['id', 'date_envoi']
