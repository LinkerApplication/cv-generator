from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class OnlyUserProfileOrReadOnlyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return bool(request.method in SAFE_METHODS
                    or request.user and request.user.is_authenticated
                    and (obj.user == request.user))


class CreateExperiencePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return bool(request.user and request.user.is_authenticated and request.user.profile)


class ExperienceUpdateDestroyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return bool(request.user and request.user.is_authenticated
                    and (obj.profile == request.user.profile)
                    and request.user.profile)


class CreateProfileOnlyOneTime(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and not request.user.profile)
