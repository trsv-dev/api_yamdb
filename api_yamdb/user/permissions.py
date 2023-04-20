from rest_framework import permissions
from rest_framework.permissions import BasePermission


class Admin(BasePermission):
    """
    Пермишн админа или суперпользователя
    для работы с Reviews, Comments.
    """

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin or request.user.is_superuser)
