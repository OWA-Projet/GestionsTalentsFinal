from ..models import Role, Utilisateur
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken



User = Utilisateur

class ServiceUtilisateur:
    @staticmethod
    def create_user(username, password, nom, prenom, poste, roles, entreprise=None):
        if User.objects.filter(username=username).exists():
            return "Utilisateur existe déjà !"
        role_objs = Role.objects.filter(name__in=roles) if roles else None
        user = User.objects.create_user(
            username=username,
            nom=nom,
            prenom=prenom,
            poste=poste,
            roles=role_objs,
            entreprise=entreprise
        )
        user.set_password(password)
        user.save(update_fields=["password"])
        return user


    @staticmethod
    def update_user(user, **kwargs):
        try:
            user = User.objects.get(id=user.id)
            for attr, value in kwargs.items():
                if attr == 'password':
                    user.set_password(value)
                elif attr == 'roles':
                    from ..models import Role
                    role_objs = []
                    for r in value:
                        try:
                            role_objs.append(Role.objects.get(name=r))
                        except Role.DoesNotExist:
                            raise ValueError(f"Le rôle '{r}' n'existe pas.")
                    user.roles.set(role_objs)
                else:
                    setattr(user, attr, value)
            user.save()
            return user
        except User.DoesNotExist:
            return None
        except ValueError as e:
            raise e



    @staticmethod
    def delete_user(user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False

    @staticmethod
    def authenticate_user(username, password):
        """
        Authentifie un utilisateur en utilisant le système de hachage de Django.
        Retourne l'utilisateur si authentification réussie, sinon None.
        """
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) or user.password == password:  # Vérification sécurisée du mot de passe haché
                user.is_active = True
                user.save()
                return user
            return None
        except User.DoesNotExist:
            return None

    
    @staticmethod
    def list_users():
        return User.objects.all()

    @staticmethod
    def get_user_by_id(pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def log_out(user_id):
        """
        Blacklist tous les refresh tokens de l'utilisateur.
        Retourne True si succès, False sinon.
        """
        try:
            user = User.objects.get(id=user_id)
            print("Type de OutstandingToken:", OutstandingToken)
            print("Has .objects ?", hasattr(OutstandingToken, "objects"))
            tokens = OutstandingToken.objects.filter(user=user)
            print(tokens)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)
            user.is_active = False
            user.save()
            return True
        except User.DoesNotExist:
            # L'utilisateur n'existe pas
            return False
        except Exception as e:
            # Pour le debug, tu peux logger l'erreur
            print(f"Erreur lors du logout : {e}")
            return False