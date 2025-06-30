# views/MetierViewSet.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from ..models import Metier
from ..serializers.MetierSerializer import MetierSerializer
from ..services.ServiceMetier import ServiceMetier

class MetierViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            metiers = ServiceMetier.list_all()
            serializer = MetierSerializer(metiers, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"detail": f"Erreur lors de la récupération des métiers : {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        metier = ServiceMetier.retrieve(pk)
        if not metier:
            return Response(
                {"detail": "Métier introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            serializer = MetierSerializer(metier)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"detail": f"Erreur lors de la sérialisation du métier : {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request):
        serializer = MetierSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            metier = ServiceMetier.create(serializer.validated_data)
            return Response(
                MetierSerializer(metier).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"detail": f"Erreur lors de la création du métier : {e}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk=None):
        metier = ServiceMetier.retrieve(pk)
        if not metier:
            return Response(
                {"detail": "Métier introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = MetierSerializer(metier, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            updated = ServiceMetier.update(metier, serializer.validated_data)
            return Response(MetierSerializer(updated).data)
        except Exception as e:
            return Response(
                {"detail": f"Erreur lors de la mise à jour du métier : {e}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk=None):
        metier = ServiceMetier.retrieve(pk)
        if not metier:
            return Response(
                {"detail": "Métier introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            ServiceMetier.delete(metier)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"detail": f"Erreur lors de la suppression du métier : {e}"},
                status=status.HTTP_400_BAD_REQUEST
            )
