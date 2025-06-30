from ..services.ServiceUtilisateur import ServiceUtilisateur
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response(
                {"detail": "Utilisateur non authentifié ou inexistant."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            success = ServiceUtilisateur.log_out(user_id)
            if success:
                return Response(
                    {"detail": "Déconnexion réussie."},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail": "Utilisateur introuvable ou déjà déconnecté."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"detail": f"Erreur inattendue lors de la déconnexion : {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
