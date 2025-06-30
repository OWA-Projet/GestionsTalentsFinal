from ..services.permissions import HasUserRole
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.ServicePostuler import ServicePostuler
from ..services.permissions import permissions

class PostulerOffreAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasUserRole.with_roles('CANDIDAT')]

    def post(self, request, *args, **kwargs):
        utilisateur = request.user
        offre_id = request.data.get('offre_id')
        cv_id = request.data.get('cv_id')

        # Vérifie présence des paramètres requis
        if not offre_id or not cv_id:
            return Response(
                {'detail': "Paramètres 'offre_id' et 'cv_id' requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            success = ServicePostuler.postuler(utilisateur, offre_id, cv_id)
            if success:
                return Response(
                    {'detail': "Postulation enregistrée."},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'detail': "Vous avez déjà postulé à cette offre avec ce CV."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'detail': f"Erreur inattendue lors de la postulation : {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

