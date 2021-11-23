import pytest
from rest_framework.serializers import ValidationError
from contextlib import nullcontext as does_not_raise_exception
from generator.profile.validators import validate_until_is_after_since


@pytest.mark.parametrize(
    "since, until, expectation",
    [
        ("2021-04-02", "2021-04-03", does_not_raise_exception()),
        ("2021-04-02", None, does_not_raise_exception()),
        ("2021-04-02", "2021-04-02", does_not_raise_exception()),
        ("2021-04-02", "2021-04-01", pytest.raises(ValidationError)),
        (None, "2021-04-02", pytest.raises(ValidationError)),
        (None, None, pytest.raises(ValidationError)),
    ],
)
def test_validate_until_is_after_since(since: str, until: str, expectation):
    with expectation:
        validate_until_is_after_since(since, until)
