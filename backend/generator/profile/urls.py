from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"profile", views.ProfileViewSet, basename="profile")
router.register(r"experience", views.ExperienceViewSet, basename="experience")


urlpatterns = [
    path("", include(router.urls)),
]
