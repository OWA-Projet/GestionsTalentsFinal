# CustomTokenObtainPairSerializer.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["roles"] = list(user.roles.values_list("name", flat=True))
        token["full_name"] = f"{user.prenom} {user.nom}"
        return token
