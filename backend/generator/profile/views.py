from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Experience, Profile
from .permissions import CanModifyProfileOrReadOnly, ModifyExperienceOrReadOnlyPermission
from .serializers import ExperienceSerializer, ProfileSerializer
from .services import user_can_create_experience, user_can_create_profile


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
    permission_classes = [CanModifyProfileOrReadOnly]

    def create(self, request, *args, **kwargs):
        if not user_can_create_profile(request):
            return Response(status=400)

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
    permission_classes = [ModifyExperienceOrReadOnlyPermission]

    def create(self, request, *args, **kwargs):
        if not user_can_create_experience(request):
            return Response(status=400)

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer) -> None:
        serializer.save(profile=self.request.user.profile)
