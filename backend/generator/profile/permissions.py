from rest_framework import permissions


class OnlyUserProfileOrReadOnlyPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return bool(request.user.is_authenticated and (obj.user == request.user))


class CreateExperiencePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        try:
            has_profile = request.user.profile
        except Exception:
            has_profile = False

        return bool(request.user and request.user.is_authenticated and has_profile)


class ExperienceRetrieveUpdateDestroyPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        try:
            has_profile = request.user.profile
        except Exception:
            has_profile = False

        return bool(
            request.user and request.user.is_authenticated and has_profile and (obj.profile == request.user.profile)
        )


class CreateProfileOnlyOneTime(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            has_profile = request.user.profile
        except Exception:
            has_profile = False

        return bool(request.user and request.user.is_authenticated and not has_profile)
