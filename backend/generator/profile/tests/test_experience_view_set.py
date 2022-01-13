from typing import Type

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from generator.user.tests.factories import UserFactory

from .factories import ExperienceFactory, ProfileFactory

EXPERIENCE_DATA = {
    "description": "experience.description",
    "employer": "experience.employer",
    "position": "experience.position",
    "since": "2021-04-02",
    "until": "",
}


@pytest.mark.django_db
def test_get_experience_retrieve(
    experience_factory: Type[ExperienceFactory],
    profile_factory: Type[ProfileFactory],
    registered_api_client: APIClient,
):
    profile = profile_factory()
    profile.user = registered_api_client.handler._force_user
    profile.save()

    experience = experience_factory(profile=profile)

    response = registered_api_client.get(reverse("experience-detail", kwargs={"pk": experience.id}))

    assert response.status_code == 200
    assert response.data == {
        "description": experience.description,
        "employer": experience.employer,
        "position": experience.position,
        "since": str(experience.since),
        "until": None,
    }


@pytest.mark.django_db
def test_post_experience_create(
    profile_factory: Type[ProfileFactory],
    registered_api_client: APIClient,
):
    profile = profile_factory()
    profile.user = registered_api_client.handler._force_user
    profile.save()

    response = registered_api_client.post(reverse("experience-list"), data=EXPERIENCE_DATA)

    assert response.status_code == 201


@pytest.mark.django_db
@pytest.mark.parametrize("anonymous, status_code", [(False, 400), (True, 401)])
def test_post_user_doesnt_have_profile_create_experience(
    registered_api_client: APIClient,
    api_client: APIClient,
    anonymous: bool,
    status_code: int,
):
    if not anonymous:
        client = registered_api_client
    else:
        api_client.force_authenticate(None, None)
        client = api_client

    response = client.post(reverse("experience-list"), data=EXPERIENCE_DATA)

    assert response.status_code == status_code


@pytest.mark.django_db
def test_update_delete_experience(
    experience_factory: Type[ExperienceFactory],
    profile_factory: Type[ProfileFactory],
    registered_api_client: APIClient,
):
    profile = profile_factory()
    profile.user = registered_api_client.handler._force_user

    experience = experience_factory(profile=profile)

    response = registered_api_client.patch(
        reverse("experience-detail", kwargs={"pk": experience.id}), data={"since": "1970-01-01"}
    )
    assert response.status_code == 200

    response = registered_api_client.delete(reverse("experience-detail", kwargs={"pk": experience.id}))

    assert response.status_code == 204


@pytest.mark.django_db
@pytest.mark.parametrize("anonymous, status_code", [(False, 403), (True, 401)])
def test_user_who_not_create_profile_trying_to_update_delete_experience(
    experience_factory: Type[ExperienceFactory],
    user_factory: Type[UserFactory],
    profile_factory: Type[ProfileFactory],
    registered_api_client: APIClient,
    api_client: APIClient,
    anonymous: bool,
    status_code: int,
):
    profile = profile_factory()
    if not anonymous:
        user = user_factory()
        profile.user = user
        client = registered_api_client
    else:
        api_client.force_authenticate(None, None)
        client = api_client

    experience = experience_factory(profile=profile)

    response = client.patch(reverse("experience-detail", kwargs={"pk": experience.id}), data={"since": "1970-01-01"})

    assert response.status_code == status_code

    response = client.delete(reverse("experience-detail", kwargs={"pk": experience.id}))

    assert response.status_code == status_code


@pytest.mark.django_db
def test_user_has_profile_but_experience_is_not_him_update_delete_experience(
    experience_factory: Type[ExperienceFactory],
    user_factory: Type[UserFactory],
    profile_factory: Type[ProfileFactory],
    registered_api_client: APIClient,
):
    profile = profile_factory()
    user = user_factory()
    profile.user = user
    experience = experience_factory(profile=profile)

    response = registered_api_client.patch(
        reverse("experience-detail", kwargs={"pk": experience.id}), data={"since": "1970-01-01"}
    )

    assert response.status_code == 403

    response = registered_api_client.delete(reverse("experience-detail", kwargs={"pk": experience.id}))

    assert response.status_code == 403
