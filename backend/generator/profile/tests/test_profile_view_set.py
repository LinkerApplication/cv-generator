from typing import Type

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from generator.user.tests.factories import UserFactory

from .factories import ExperienceFactory, ProfileFactory

PROFILE_DATA = {
    "email": "mail@mail.ru",
    "full_name": "Hello Ivanov",
    "number": "+798743232",
    "about_me": "Yes",
    "website": "https://www.twitch.tv/",
    "experiences": [],
}


@pytest.mark.django_db
def test_get_profile_retrieve(
    experience_factory: Type[ExperienceFactory],
    profile_factory: Type[ProfileFactory],
    registered_api_client: APIClient,
):
    profile = profile_factory()
    profile.user = registered_api_client.handler._force_user
    profile.save()

    experience = experience_factory(profile=profile)
    response = registered_api_client.get(reverse("profile-detail", kwargs={"pk": profile.id}))

    assert response.status_code == 200
    assert response.data == {
        "email": profile.email,
        "full_name": profile.full_name,
        "number": profile.number,
        "about_me": profile.about_me,
        "website": profile.website,
        "experiences": [
            {
                "description": experience.description,
                "employer": experience.employer,
                "position": experience.position,
                "since": str(experience.since),
                "until": None,
            },
        ],
        "pk": profile.pk,
    }


def _try_change_profile_detail(profile_id: int, status_code: int, client: APIClient):
    response = client.patch(reverse("profile-detail", kwargs={"pk": profile_id}), data={"email": "lala@mail.ru"})
    assert response.status_code == status_code

    response = client.delete(reverse("profile-detail", kwargs={"pk": profile_id}))
    assert response.status_code == status_code


@pytest.mark.django_db
def test_user_who_not_create_profile_trying_to_update_delete_profile_registered(
    profile_factory: Type[ProfileFactory],
    user_factory: Type[UserFactory],
    registered_api_client: APIClient,
):
    profile = profile_factory()
    user = user_factory()
    profile.user = user

    _try_change_profile_detail(profile.id, status.HTTP_403_FORBIDDEN, registered_api_client)


@pytest.mark.django_db
def test_user_who_not_create_profile_trying_to_update_delete_profile_anonymous(
    profile_factory: Type[ProfileFactory],
    api_client: APIClient,
):
    profile = profile_factory()

    _try_change_profile_detail(profile.id, status.HTTP_401_UNAUTHORIZED, api_client)


@pytest.mark.django_db
def test_post_profile_create(
    registered_api_client: APIClient,
):
    response = registered_api_client.post(reverse("profile-list"), data=PROFILE_DATA)

    assert response.status_code == 201


@pytest.mark.django_db
def test_user_has_profile_trying_to_create_second_profile(
    profile_factory: Type[ProfileFactory],
    registered_api_client: APIClient,
):
    profile = profile_factory()
    profile.user = registered_api_client.handler._force_user

    response = registered_api_client.post(reverse("profile-list"), data=PROFILE_DATA)
    assert response.status_code == 400


@pytest.mark.django_db
def test_anonymous_user_trying_to_create_profile(api_client: APIClient):
    response = api_client.post(reverse("profile-list"), data=PROFILE_DATA)
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_delete_profile(
    profile_factory: Type[ProfileFactory],
    registered_api_client: APIClient,
):
    profile = profile_factory()
    profile.user = registered_api_client.handler._force_user
    profile.save()

    response = registered_api_client.patch(
        reverse("profile-detail", kwargs={"pk": profile.id}), data={"email": "lala@mail.ru"}
    )

    assert response.status_code == 200

    response = registered_api_client.delete(reverse("profile-detail", kwargs={"pk": profile.id}))

    assert response.status_code == 204
