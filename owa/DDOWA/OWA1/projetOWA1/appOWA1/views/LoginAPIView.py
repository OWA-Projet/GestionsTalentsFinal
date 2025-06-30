# appOWA1/views/LoginAPIView.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from ..serializers.auth import LoginSerializer
from ..serializers.UtilisateurSerializer import UtilisateurSerializer
from ..services.ServiceUtilisateur import ServiceUtilisateur
from ..services.CustomTokenObtainPairSerializer import CustomTokenObtainPairSerializer


class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes     = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(
                {"detail": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = ServiceUtilisateur.authenticate_user(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            if not user:
                return Response(
                    {"detail": "Identifiants invalides !"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            if hasattr(user, "is_active") and not user.is_active:
                return Response(
                    {"detail": "Votre compte est désactivé."},
                    status=status.HTTP_403_FORBIDDEN
                )

            # JWT
            refresh = CustomTokenObtainPairSerializer.get_token(user)

            user_data = UtilisateurSerializer(user).data
            # print(user_data) # En production, commenter pour éviter fuite info

            return Response(
                {
                    "refresh": str(refresh),
                    "access":  str(refresh.access_token),
                    "user":    user_data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": f"Erreur inattendue lors de la connexion : {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
