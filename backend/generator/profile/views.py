from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Experience, Profile
from .permissions import (
    CreateExperiencePermission,
    CreateProfileOnlyOneTime,
    ExperienceRetrieveUpdateDestroyPermission,
    OnlyUserProfileOrReadOnlyPermission,
)
from .serializers import ProfileSerializer, SerializerExperience


class ProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [OnlyUserProfileOrReadOnlyPermission]
    permission_class_action_mapping = {"create": [CreateProfileOnlyOneTime]}

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        return [
            permission()
            for permission in self.permission_class_action_mapping.get(self.action, self.permission_classes)
        ]


class ExperienceViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Experience.objects.all()
    serializer_class = SerializerExperience
    permission_classes = [ExperienceRetrieveUpdateDestroyPermission]
    permission_class_action_mapping = {"create": [CreateExperiencePermission]}

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    def get_permissions(self):
        print(self.action)
        return [
            permission()
            for permission in self.permission_class_action_mapping.get(self.action, self.permission_classes)
        ]
