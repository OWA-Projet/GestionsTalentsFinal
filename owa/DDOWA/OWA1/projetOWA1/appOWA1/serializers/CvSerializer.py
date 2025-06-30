from rest_framework import serializers
from ..models import CV, Metier, OffresEmploi,Utilisateur
from .UtilisateurSerializer import UtilisateurSerializer
class MetierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metier
        fields = ['id', 'nom', 'description']

from rest_framework import serializers

           # adapte les chemins si besoin
  # <-- le tien !

class CVSerializer(serializers.ModelSerializer):
    owner = UtilisateurSerializer(read_only=True)  # ← Objet complet à la lecture
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=Utilisateur.objects.all(), write_only=True, source='owner'
    )

    metier = serializers.PrimaryKeyRelatedField(
        queryset=Metier.objects.all(), write_only=True, allow_null=True, required=False
    )
    metier_detail = MetierSerializer(source='metier', read_only=True)

    offres = serializers.PrimaryKeyRelatedField(
        queryset=OffresEmploi.objects.all(), many=True, required=False
    )

    class Meta:
        model = CV
        fields = [
            "id",
            "owner",          # ← Objet complet pour lecture front
            "owner_id",       # ← id pour écriture (POST, PATCH)
            "texte_brut",
            "fichier",
            "uploaded_at",
            "is_classe",
            "formations",
            "experiences",
            "competences",
            "langues",
            "permis_conduite",
            "metier",         # ← id du métier (POST, PATCH)
            "metier_detail",  # ← détails métier pour lecture
            "offres",
        ]
        read_only_fields = [
            "id", "uploaded_at", "is_classe", "owner", "metier_detail"
        ]
