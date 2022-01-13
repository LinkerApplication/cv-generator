from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Experience, Profile
from .permissions import HasProfileAndIsOwnerPermission, IsProfileOwnerPermission
from .serializers import ExperienceSerializer, ProfileSerializer
from .services import check_user_has_profile, get_user_profile


class ProfileViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    Set of Profile controllers.

    Creating profile. One user can has only one profile.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsProfileOwnerPermission]

    def create(self, request, *args, **kwargs):
        if not check_user_has_profile(request.user):
            return Response(
                {"error": "Cannot create profile, when you have profile already"}, status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)


class ExperienceViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    Set of Experience controllers.

    Creating experience. User can create experience if he has profile.
    User can create many experiences.
    """

    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, HasProfileAndIsOwnerPermission]

    def create(self, request, *args, **kwargs):
        profile = get_user_profile(request.user.pk)
        if not profile:
            return Response(
                {"error": "Cannot create experience, when you don't have profile"}, status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer) -> None:
        serializer.save(profile=self.request.user.profile)
