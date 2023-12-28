from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS
)


class IsAdminOrReadOnly(BasePermission):
    """Права доступа для админа."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user.is_authenticated and request.user.is_admin
        )
