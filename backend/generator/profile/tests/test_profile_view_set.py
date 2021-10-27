from collections import OrderedDict
from typing import Type

import pytest
from django.urls import reverse
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
    registered_api_client.handler._force_user.save()
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
        "user": profile.user.email,
        "experiences": [
            OrderedDict(
                [
                    ("description", experience.description),
                    ("employer", experience.employer),
                    ("position", experience.position),
                    ("since", str(experience.since)),
                    ("until", (experience.until if experience.until is None else str(experience.until))),
                ]
            )
        ],
        "pk": profile.pk,
    }


@pytest.mark.django_db
@pytest.mark.parametrize("anonymous", [(False,), (True,)])
def test_user_who_not_create_profile_get_profile_retrieve(
    profile_factory: Type[ProfileFactory],
    user_factory: Type[UserFactory],
    registered_api_client: APIClient,
    api_client: APIClient,
    anonymous: bool,
):
    profile = profile_factory()
    if not anonymous:
        user = user_factory()
        user.save()
        profile.user = user
        client = registered_api_client
    else:
        client = api_client
    profile.save()

    response = client.get(reverse("profile-detail", kwargs={"pk": profile.id}))

    assert response.status_code == 403


@pytest.mark.django_db
def test_post_profile_create(
    registered_api_client: APIClient,
):
    registered_api_client.handler._force_user.save()
    response = registered_api_client.post(reverse("profile-list"), data=PROFILE_DATA)

    assert response.status_code == 201
    assert response.data["user"] == registered_api_client.handler._force_user.email


@pytest.mark.django_db
def test_user_has_profile_trying_to_create_second_profile(
    profile_factory: Type[ProfileFactory],
    registered_api_client: APIClient,
):
    profile = profile_factory()
    registered_api_client.handler._force_user.save()
    profile.user = registered_api_client.handler._force_user
    profile.save()

    response = registered_api_client.post(reverse("profile-list"), data=PROFILE_DATA)

    assert response.status_code == 403


@pytest.mark.django_db
def test_anonymous_user_trying_to_create_profile(api_client: APIClient):
    response = api_client.post(reverse("profile-list"), data=PROFILE_DATA)

    assert response.status_code == 403


@pytest.mark.django_db
def test_update_delete_profile(
    profile_factory: Type[ProfileFactory],
    registered_api_client: APIClient,
):
    profile = profile_factory()
    registered_api_client.handler._force_user.save()
    profile.user = registered_api_client.handler._force_user
    profile.save()

    response = registered_api_client.patch(
        reverse("profile-detail", kwargs={"pk": profile.id}), data={"email": "lala@mail.ru"}
    )

    assert response.status_code == 200

    response = registered_api_client.delete(reverse("profile-detail", kwargs={"pk": profile.id}))

    assert response.status_code == 204


@pytest.mark.django_db
@pytest.mark.parametrize("anonymous", [(False,), (True,)])
def test_user_who_not_create_profile_trying_to_update_delete_profile(
    profile_factory: Type[ProfileFactory],
    user_factory: Type[UserFactory],
    registered_api_client: APIClient,
    api_client: APIClient,
    anonymous: bool,
):
    profile = profile_factory()
    if not anonymous:
        user = user_factory()
        user.save()
        profile.user = user
        client = registered_api_client
    else:
        client = api_client

    profile.save()

    response = client.patch(reverse("profile-detail", kwargs={"pk": profile.id}), data={"email": "lala@mail.ru"})

    assert response.status_code == 403

    response = client.delete(reverse("profile-detail", kwargs={"pk": profile.id}))

    assert response.status_code == 403
