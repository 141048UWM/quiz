from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return (
            obj.owner == request.user or
            getattr(obj, 'user', None) == request.user
        )