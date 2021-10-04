from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
     extend the BasePermission,overwrite its has_object_permission method,
     check if the user  is requesting read-only access and return True
     Otherwise, we’ll return True only if the  user making the request owns the profile
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user