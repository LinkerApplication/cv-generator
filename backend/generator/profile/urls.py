from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"profiles", views.ProfileViewSet, basename="profile")
router.register(r"experiences", views.ExperienceViewSet, basename="experience")


urlpatterns = [
    path("", include(router.urls)),
]
