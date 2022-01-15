from typing import Type

import pytest
from django.urls import reverse
from rest_framework import status
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


def _try_create_experience(status_code: int, client: APIClient):
    response = client.post(reverse("experience-list"), data=EXPERIENCE_DATA)

    assert response.status_code == status_code


@pytest.mark.django_db
def test_post_user_doesnt_have_profile_create_experience_registered(
    registered_api_client: APIClient,
):
    _try_create_experience(status.HTTP_400_BAD_REQUEST, registered_api_client)


@pytest.mark.django_db
def test_post_user_doesnt_have_profile_create_experience_anonymous(
    api_client: APIClient,
):
    _try_create_experience(status.HTTP_401_UNAUTHORIZED, api_client)


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


def _try_update_and_delete_experience(
    experience_id, status_code: int, client: APIClient, experience_factory: Type[ExperienceFactory]
):

    response = client.patch(reverse("experience-detail", kwargs={"pk": experience_id}), data={"since": "1970-01-01"})
    assert response.status_code == status_code

    response = client.delete(reverse("experience-detail", kwargs={"pk": experience_id}))
    assert response.status_code == status_code


@pytest.mark.django_db
def test_user_who_not_create_profile_trying_to_update_delete_experience_registered(
    experience_factory: Type[ExperienceFactory],
    user_factory: Type[UserFactory],
    profile_factory: Type[ProfileFactory],
    registered_api_client: APIClient,
):
    profile = profile_factory()

    user = user_factory()
    profile.user = user
    experience = experience_factory(profile=profile)

    _try_update_and_delete_experience(
        experience.id, status.HTTP_403_FORBIDDEN, registered_api_client, experience_factory
    )


@pytest.mark.django_db
def test_user_who_not_create_profile_trying_to_update_delete_experience_anonymous(
    experience_factory: Type[ExperienceFactory],
    profile_factory: Type[ProfileFactory],
    api_client: APIClient,
):
    profile = profile_factory()
    experience = experience_factory(profile=profile)

    _try_update_and_delete_experience(experience.id, status.HTTP_401_UNAUTHORIZED, api_client, experience_factory)


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

    _try_update_and_delete_experience(
        experience.id, status.HTTP_403_FORBIDDEN, registered_api_client, experience_factory
    )
