from ..serializers.OffresEmploiSerializer import OffresEmploiSerializer
from ..services.ServiceOffresEmploi import ServiceOffresEmploi
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import Http404

class OffresAcceuilViewSet(viewsets.ViewSet):
    """
    Vue lecture seule des offres d'emploi (accueil/public).
    """

    def list(self, request):
        try:
            emplois = ServiceOffresEmploi.list_all()
            serializer = OffresEmploiSerializer(emplois, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"detail": f"Erreur lors de la récupération des offres : {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        try:
            emploi = ServiceOffresEmploi.retrieve(pk)
            serializer = OffresEmploiSerializer(emploi)
            return Response(serializer.data)
        except Http404:
            return Response(
                {"detail": "Offre non trouvée."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": f"Erreur lors de la récupération de l'offre : {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
