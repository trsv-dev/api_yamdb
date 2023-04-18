from rest_framework import permissions
from rest_framework.permissions import BasePermission


class AdminUserOrReadOnly(permissions.BasePermission):
    """Пермишн для работы с Genres и Categories."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return request.user.is_admin
        return False


class AdminModeratorAuthorOrReadOnly(BasePermission):
    """Пермишн для работы с Reviews и Comments."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator)


class AdminUser(permissions.BasePermission):
    """Пермишн для работы с Users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.is_admin or request.user.is_superuser
        )


class AdminUserOnly(permissions.BasePermission):
    """Пермишн для работы с Genres и Categories."""
    def has_permission(self, request, view):
        return request.user.is_admin
