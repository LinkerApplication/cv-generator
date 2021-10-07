from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import Profile, Experience
from .serializers import (ProfileSerializer,
                          SerializerCreateExperience)
from .permissions import (OnlyUserProfileOrReadOnlyPermission,
                          ExperienceUpdateDestroyPermission, CreateExperiencePermission, CreateProfileOnlyOneTime)


class CreateView(generics.CreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [CreateProfileOnlyOneTime]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileUpdateDestroyRetrieveView(generics.RetrieveAPIView,
                                       generics.UpdateAPIView,
                                       generics.DestroyAPIView):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [OnlyUserProfileOrReadOnlyPermission]


class CreateExperienceView(generics.CreateAPIView):
    serializer_class = SerializerCreateExperience
    permission_classes = [CreateExperiencePermission]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class ExperienceUpdateDestroyView(generics.RetrieveAPIView,
                                  generics.UpdateAPIView,
                                  generics.DestroyAPIView):

    queryset = Experience.objects.all()
    serializer_class = SerializerCreateExperience
    permission_classes = [ExperienceUpdateDestroyPermission]
