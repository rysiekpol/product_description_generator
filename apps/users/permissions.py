from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """
    Allows access only to superusers.
    """

    def has_permission(self, request, view):
        return request.user.is_super
