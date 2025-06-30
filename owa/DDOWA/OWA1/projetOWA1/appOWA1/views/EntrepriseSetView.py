from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from ..models import Entreprise
from ..serializers.EntrepriseSerializer import EntrepriseSerializer
from ..services.ServiceEntreprise import ServiceEntreprise

class EntrepriseViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        try:
            entreprises = ServiceEntreprise.list_all()
            serializer = EntrepriseSerializer(entreprises, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la récupération des entreprises : {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        entreprise = ServiceEntreprise.retrieve(pk)
        if not entreprise:
            return Response({"detail": "Entreprise introuvable."}, status=status.HTTP_404_NOT_FOUND)
        try:
            serializer = EntrepriseSerializer(entreprise)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la sérialisation de l'entreprise : {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        serializer = EntrepriseSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            entreprise = ServiceEntreprise.create(serializer.validated_data)
            return Response(EntrepriseSerializer(entreprise).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la création de l'entreprise : {e}"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        entreprise = ServiceEntreprise.retrieve(pk)
        if not entreprise:
            return Response({"detail": "Entreprise introuvable."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EntrepriseSerializer(entreprise, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            updated = ServiceEntreprise.update(entreprise, serializer.validated_data)
            return Response(EntrepriseSerializer(updated).data)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la mise à jour de l'entreprise : {e}"}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        entreprise = ServiceEntreprise.retrieve(pk)
        if not entreprise:
            return Response({"detail": "Entreprise introuvable."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EntrepriseSerializer(entreprise, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            updated = ServiceEntreprise.update(entreprise, serializer.validated_data)
            return Response(EntrepriseSerializer(updated).data)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la mise à jour partielle de l'entreprise : {e}"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        entreprise = ServiceEntreprise.retrieve(pk)
        if not entreprise:
            return Response({"detail": "Entreprise introuvable."}, status=status.HTTP_404_NOT_FOUND)
        try:
            ServiceEntreprise.delete(entreprise)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la suppression de l'entreprise : {e}"}, status=status.HTTP_400_BAD_REQUEST)
