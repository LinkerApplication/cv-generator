from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import Profile, Experience
from .serializers import (ProfileSerializer,
                          SerializerCreateExperience)
from .permissions import (OnlyUserProfileOrReadOnlyPermission,
                          ExperienceUpdateDestroyPermission, CreateExperiencePermission)


class CreateView(mixins.CreateModelMixin,
                 GenericViewSet):

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileUpdateDestroyRetrieveView(mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin,
                                       GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [OnlyUserProfileOrReadOnlyPermission]




class CreateExperienceView(mixins.CreateModelMixin,
                           GenericViewSet):

    serializer_class = SerializerCreateExperience
    permission_classes = [CreateExperiencePermission]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class ExperienceUpdateDestroyView(mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin,
                                  GenericViewSet):

    queryset = Experience.objects.all()
    serializer_class = SerializerCreateExperience
    permission_classes = [ExperienceUpdateDestroyPermission]
