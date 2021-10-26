import pytest

from typing import Type

from django.urls import reverse
from rest_framework.test import APIClient

from .factories import ProfileFactory, ExperienceFactory


@pytest.mark.django_db
def test_get_profile_retrieve(
        experience_factory: Type[ExperienceFactory],
        configured_api_client: APIClient,
):
    profile = experience_factory()
    response = configured_api_client.get(reverse('profile-retrieve', kwargs={'pk': profile.profile.id}))

    assert response.status_code == 200
    assert response.data == {
        "email": profile.profile.email,
        "full_name": profile.profile.full_name,
        "number": profile.profile.number,
        "about_me": profile.profile.about_me,
        "website": profile.profile.website,
        "user": profile.profile.user,
        "experiences": [{
            "description": profile.description,
            "employer": profile.employer,
            "position": profile.position,
            "since": profile.since,
            "until": profile.until,
        }],
        "since": profile.profile.since,
        "until": profile.profile.until,
        "pk": profile.profile.pk,
    }
