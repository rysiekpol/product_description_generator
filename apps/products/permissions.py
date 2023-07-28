from rest_framework import permissions


class IsProductAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow product authors to edit them.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of a product.
        return obj.created_by == request.user
