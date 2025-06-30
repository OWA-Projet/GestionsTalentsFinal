from ..services.permissions import HasUserRole
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..models import Utilisateur
from ..serializers.UtilisateurSerializer import UtilisateurSerializer
from ..services.ServiceUtilisateur import ServiceUtilisateur
from ..models import Entreprise, Role

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,  HasUserRole.with_roles('ADMIN')]  # à adapter si tu veux limiter à l'admin

    def list(self, request):
        try:
            users = ServiceUtilisateur.list_users()
            serializer = UtilisateurSerializer(users, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': f'Erreur lors de la récupération des utilisateurs : {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        user = ServiceUtilisateur.get_user_by_id(pk)
        if not user:
            return Response({'detail': 'Utilisateur introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UtilisateurSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        serializer = UtilisateurSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            entreprise = None
            if 'entreprise' in data and data['entreprise']:
                try:
                    entreprise = Entreprise.objects.get(pk=data['entreprise'].id if hasattr(data['entreprise'], 'id') else data['entreprise'])
                except Entreprise.DoesNotExist:
                    return Response({'detail': "Entreprise introuvable."}, status=400)
            roles = data.get('roles', [])
            # Roles peut être une liste de noms ou d'IDs
            if roles and isinstance(roles[0], str):
                roles = [r for r in roles]
            else:
                roles = [r.name if hasattr(r, "name") else str(r) for r in roles]
            result = ServiceUtilisateur.create_user(
                username=data['username'],
                password=data.get('password', 'changeme123'),  # à adapter selon le frontend
                nom=data['nom'],
                prenom=data['prenom'],
                poste=data.get('poste', ''),
                roles=roles,
                entreprise=entreprise
            )
            if isinstance(result, str):
                return Response({'detail': result}, status=400)
            return Response(UtilisateurSerializer(result).data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        user = ServiceUtilisateur.get_user_by_id(pk)
        if not user:
            return Response({'detail': 'Utilisateur introuvable.'}, status=404)
        serializer = UtilisateurSerializer(user, data=request.data, partial=False)
        if serializer.is_valid():
            data = serializer.validated_data
            entreprise = None
            if 'entreprise' in data and data['entreprise']:
                try:
                    entreprise = Entreprise.objects.get(pk=data['entreprise'].id if hasattr(data['entreprise'], 'id') else data['entreprise'])
                except Entreprise.DoesNotExist:
                    return Response({'detail': "Entreprise introuvable."}, status=400)
            roles = data.get('roles', [])
            if roles and isinstance(roles[0], str):
                roles = [r for r in roles]
            else:
                roles = [r.name if hasattr(r, "name") else str(r) for r in roles]
            user = ServiceUtilisateur.update_user(
                user,
                username=data.get('username', user.username),
                nom=data.get('nom', user.nom),
                prenom=data.get('prenom', user.prenom),
                poste=data.get('poste', user.poste),
                roles=roles,
                entreprise=entreprise,
                **({'password': data['password']} if 'password' in data and data['password'] else {})
            )
            return Response(UtilisateurSerializer(user).data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        user = ServiceUtilisateur.get_user_by_id(pk)
        if not user:
            return Response({'detail': 'Utilisateur introuvable.'}, status=404)
        serializer = UtilisateurSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            data = serializer.validated_data
            entreprise = None
            if 'entreprise' in data and data['entreprise']:
                try:
                    entreprise = Entreprise.objects.get(pk=data['entreprise'].id if hasattr(data['entreprise'], 'id') else data['entreprise'])
                except Entreprise.DoesNotExist:
                    return Response({'detail': "Entreprise introuvable."}, status=400)
            roles = data.get('roles', [])
            if roles and isinstance(roles[0], str):
                roles = [r for r in roles]
            else:
                roles = [r.name if hasattr(r, "name") else str(r) for r in roles]
            user = ServiceUtilisateur.update_user(
                user,
                username=data.get('username', user.username),
                nom=data.get('nom', user.nom),
                prenom=data.get('prenom', user.prenom),
                poste=data.get('poste', user.poste),
                roles=roles,
                entreprise=entreprise
            )
            return Response(UtilisateurSerializer(user).data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        result = ServiceUtilisateur.delete_user(pk)
        if result:
            return Response(status=204)
        return Response({'detail': 'Utilisateur introuvable.'}, status=404)
