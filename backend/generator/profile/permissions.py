from rest_framework import permissions


class CanModifyProfileOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, profile):
        """
        Return `True` if user has profile he can modify or read profile, `False` otherwise.
        """
        return bool(request.user.is_authenticated and (profile.user == request.user))


class ModifyExperienceOrReadOnlyPermission(permissions.BasePermission):
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
