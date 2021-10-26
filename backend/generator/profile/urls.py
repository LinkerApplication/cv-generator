from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"profiles", views.ProfileViewSet, basename="profile")
router.register(r"experiences", views.ExperienceViewSet, basename="experience")
