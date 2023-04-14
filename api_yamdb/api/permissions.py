from rest_framework import permissions


class AdminUserOrReadOnly(permissions.BasePermission):
    """Пермишн для работы с Genres и Categories"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False
