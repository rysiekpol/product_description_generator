from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from .models import Product


class IsProductAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow product authors to edit them.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user
