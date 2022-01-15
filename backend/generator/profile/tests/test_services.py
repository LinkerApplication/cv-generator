from typing import Type

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import Profile
from ..services import check_user_has_profile, get_user_profile
from .factories import ProfileFactory
from .test_profile_view_set import PROFILE_DATA


@pytest.mark.django_db
def test_get_user_profile(profile_factory: Type[ProfileFactory]):
    profile = profile_factory()
    assert isinstance(get_user_profile(profile.pk), Profile)


@pytest.mark.django_db
def test_negative_get_user_profile():
    assert get_user_profile(1) is False


@pytest.mark.django_db
def test_negative_check_user_has_profile(
    registered_api_client: APIClient,
):
    assert check_user_has_profile(registered_api_client.handler._force_user) is False


@pytest.mark.django_db
def test_check_user_has_profile(
    registered_api_client: APIClient,
):
    registered_api_client.post(reverse("profile-list"), data=PROFILE_DATA)

    assert check_user_has_profile(registered_api_client.handler._force_user) is True
