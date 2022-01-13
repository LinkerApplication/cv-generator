from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsProfileOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, profile):
        """
        Return `True` if user has profile he can modify or read profile, `False` otherwise.
        """
        return bool(request.method in SAFE_METHODS or request.user.is_authenticated and (profile.user == request.user))


class HasProfileAndIsOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, experience):
        """
        Return `True` if user can modify experience or read, `False` otherwise.
        """
        has_profile = hasattr(request.user, "profile")

        return bool(
            request.user
            and request.user.is_authenticated
            and has_profile
            and experience.profile == request.user.profile
        )
