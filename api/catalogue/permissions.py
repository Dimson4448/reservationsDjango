from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Autorise les requêtes de lecture pour tout le monde,
    mais exige l'authentification pour POST, PUT et DELETE.
    """

    def has_permission(self, request, view):
        # Autorise toutes les requêtes de lecture (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Autorise POST, PUT, DELETE uniquement pour les utilisateurs authentifiés
        return request.user and request.user.is_authenticated
