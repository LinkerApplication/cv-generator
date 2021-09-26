from typing import Type

import pytest

from .factories import UserFactory, ProfileFactory


@pytest.mark.django_db
def test_profile_create(
        user_factory: Type[UserFactory],
        profile_factory: Type[ProfileFactory]
):
    profile = profile_factory.create()
    print(profile.user)
    print(profile.website)
    print(profile.number)
