from typing import List, Protocol, Tuple, Type, TypedDict, Union

import pytest
from django.contrib.auth.models import AnonymousUser, User
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import UserFactory


# TODO : Uncomment after integration custom user model
class UserMaker(Protocol):
    def __call__(self, is_registered: bool) -> Union[AnonymousUser, User]: ...


@pytest.fixture
def create_user(user_factory: Type[UserFactory]) -> UserMaker:
    """
    Fixture, which provides a registered User, if is_registered is True.
    Otherwise returns AnonymousUser.
    If is_staff is True, returns a User with admin permissions.
    """

    def make_user(is_registered: bool) -> Union[AnonymousUser, User]:
        if not is_registered:
            return AnonymousUser()
    # TODO: remove type ignore as soon as pycharm is updated to 2021.2
    return make_user  # type: ignore


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def configured_api_client(request, create_user: UserMaker, api_client: APIClient) -> APIClient:
    """
    Fixture, which returns a DRF APIClient, which takes bool parameters, provided in a request.param
        by a parametrize decorator.
    """
    is_registered = request.param
    user = create_user(is_registered=is_registered)
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def registered_api_client(create_user: UserMaker, api_client: APIClient) -> APIClient:
    api_client.force_authenticate(user=create_user(is_registered=True))
    return api_client


@pytest.fixture
def status_code(request) -> int:
    """
    Fixture, which returns a status code which is provided in the parametrize decorator.
    """
    status_code = request.param
    return status_code


AUTHENTICATION_FIXTURES = ["configured_api_client", "status_code"]


class _PyTestAuthParametrization(TypedDict):
    argnames: List[str]
    # List[(is registered, status code)]
    argvalues: List[Tuple[bool, int]]
    indirect: List[str]
    ids: List[str]


def try_all_authentications_with_codes(
        anonymous_code: int = 200,
        registered_code: int = 200,
) -> _PyTestAuthParametrization:
    """
    Used in any test cases, which simply need to check same functionality for different user permissions.
    May not be suitable for complex test cases.
    As arguments it takes status codes for each permission.
    As an output it returns a Dict, which must be unpacked inside the `parametrize` decorator.
    Returned Dict provides a sequence of tuples, corresponding to each provided status code.
    First value is bool values, which go further to configured_api_client as a request param.
    Second value of the tuple is status code, which should be a result of a request to the tested endpoint.
        That status code than goes to the stats_code fixture as a request param.
    """
    return _PyTestAuthParametrization(
        argnames=AUTHENTICATION_FIXTURES,
        argvalues=[
            # is registered, status code
            (False, anonymous_code),
            (True, registered_code),
        ],
        indirect=AUTHENTICATION_FIXTURES,
        ids=["anonymous", "registered"]
    )
