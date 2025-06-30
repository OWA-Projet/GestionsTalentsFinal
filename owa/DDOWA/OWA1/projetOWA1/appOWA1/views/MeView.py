from rest_framework.views import APIView         # <--- AJOUTE cette ligne
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..services.permissions import HasUserRole
from ..serializers.UtilisateurSerializer import UtilisateurSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user or not hasattr(user, "id"):
            return Response(
                {"detail": "Utilisateur non authentifié."},
                status=401
            )
        try:
            serializer = UtilisateurSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"detail": f"Erreur lors de la récupération du profil : {e}"},
                status=500
            )
