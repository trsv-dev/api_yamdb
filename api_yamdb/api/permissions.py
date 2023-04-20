from rest_framework import permissions
from rest_framework.permissions import BasePermission


class AdminOrReadOnly(permissions.BasePermission):
    """Пермишн для работы с Genres и Categories."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return request.user.is_admin
        return False


class Author(BasePermission):
    """Пермишн автора для работы с Reviews и Comments."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class Moderator(BasePermission):
    """Пермишн модератора для работы с Reviews и Comments."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_moderator
                or request.user.is_staff)


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
