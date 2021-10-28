from profile.tests.factories import ExperienceFactory, ProfileFactory
from typing import Protocol, Type, Union

import pytest
from django.contrib.auth.models import AnonymousUser
from pytest_factoryboy import register
from rest_framework.test import APIClient, APIRequestFactory
from user.models import User
from user.tests.factories import UserFactory

register(UserFactory)
register(ProfileFactory)
register(ExperienceFactory)


class UserMaker(Protocol):
    def __call__(self, is_registered: bool, is_staff: bool) -> Union[AnonymousUser, User]:
        ...


@pytest.fixture
def create_user(user_factory: Type[UserFactory]) -> UserMaker:
    """
    Fixture, which provides a registered User, if is_registered is True.
    Otherwise returns AnonymousUser.
    If is_staff is True, returns a User with admin permissions.
    """

    def make_user(is_registered: bool, is_staff: bool) -> Union[AnonymousUser, User]:
        if not is_registered:
            return AnonymousUser()
        return user_factory(is_staff=is_staff)

    # TODO: remove type ignore as soon as pycharm is updated to 2021.2
    return make_user  # type: ignore


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def registered_api_client(create_user: UserMaker, api_client: APIClient) -> APIClient:
    api_client.force_authenticate(user=create_user(is_registered=True, is_staff=False))
    return api_client
