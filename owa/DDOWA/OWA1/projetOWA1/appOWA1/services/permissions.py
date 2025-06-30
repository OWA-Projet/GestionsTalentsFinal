# permissions.py
from rest_framework import permissions

class HasUserRole(permissions.BasePermission):
    allowed_roles = []

    @classmethod
    def with_roles(cls, *roles):
        class CustomRolePermission(cls):
            allowed_roles = roles
        return CustomRolePermission

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
    # On récupère tous les rôles liés à l'utilisateur
        user_roles = getattr(request.user, 'roles', None)
        if user_roles is None:
            return False
    # user_roles est un ManyRelatedManager, on le parcourt avec .all()
        return any(
            role.name in self.allowed_roles
            for role in user_roles.all()
        )
