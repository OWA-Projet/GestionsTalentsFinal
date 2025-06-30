from rest_framework import serializers
from ..models import Utilisateur, Role

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    nom = serializers.CharField()
    prenom = serializers.CharField()
    poste = serializers.CharField()
    roles = serializers.ListField(
        child=serializers.CharField(), allow_empty=True
    )

    def validate_roles(self, value):
        # Vérifier que les rôles existent
        if value:
            qs = Role.objects.filter(name__in=value)
            if qs.count() != len(set(value)):
                raise serializers.ValidationError("Un ou plusieurs rôles sont invalides.")
        return value
