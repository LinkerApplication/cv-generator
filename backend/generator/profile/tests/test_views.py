from collections import OrderedDict

import pytest

from typing import Type

from django.urls import reverse
from rest_framework.test import APIClient

from .factories import ProfileFactory, ExperienceFactory


@pytest.mark.django_db
def test_get_profile_retrieve(
        experience_factory: Type[ExperienceFactory],
        profile_factory: Type[ProfileFactory],
        registered_api_client: APIClient,
):
    profile = profile_factory()
    experience = experience_factory(profile=profile)
    response = registered_api_client.get(reverse('profile-detail', kwargs={'pk': profile.id}))

    assert response.status_code == 200
    assert response.data == {
        "email": profile.email,
        "full_name": profile.full_name,
        "number": profile.number,
        "about_me": profile.about_me,
        "website": profile.website,
        "user": profile.user,
        "experiences": [OrderedDict([
            ('description', experience.description),
            ('employer', experience.employer),
            ('position', experience.position),
            ('since', str(experience.since)),
            ('until', (experience.until if experience.until is None
                       else str(experience.until)))]
        )],
        "pk": profile.pk,
    }
