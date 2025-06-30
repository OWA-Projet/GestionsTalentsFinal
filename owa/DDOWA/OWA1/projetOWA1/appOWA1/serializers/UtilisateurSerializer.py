from rest_framework import serializers
from ..models import Role, Utilisateur, Entreprise

class EntrepriseLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entreprise
        fields = ['id', 'nom']

class UtilisateurSerializer(serializers.ModelSerializer):
    roles = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Role.objects.all(),
        many=True
    )
    password = serializers.CharField(write_only=True, required=False)
    entreprise = EntrepriseLightSerializer(read_only=True)
    entreprise_id = serializers.PrimaryKeyRelatedField(
        queryset=Entreprise.objects.all(), source='entreprise', write_only=True, required=False
        , allow_null=True
    )

    class Meta:
        model = Utilisateur
        fields = [
            "id", "username", "password", "nom", "prenom", "poste", "roles",
            "entreprise", "entreprise_id", "is_staff"
        ]
        read_only_fields = ["id", "is_staff"]
        extra_kwargs = {
            "password": {"write_only": True},
        }
