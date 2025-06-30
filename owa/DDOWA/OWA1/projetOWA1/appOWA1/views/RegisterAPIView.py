from ..serializers.RegisterSerializer import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.ServiceUtilisateur import ServiceUtilisateur

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            result = ServiceUtilisateur.create_user(
                username=data['username'],
                password=data['password'],
                nom=data['nom'],
                prenom=data['prenom'],
                poste=data['poste'],
                roles=data.get('roles', [])
            )
            if isinstance(result, str):
                # Erreur personnalisée (ex: utilisateur existe déjà)
                return Response({'detail': result}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail': 'Utilisateur créé avec succès.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)