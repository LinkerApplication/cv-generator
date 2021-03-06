import datetime
from typing import Optional

from rest_framework import serializers


def validate_until_is_after_since(since: Optional[str], until: Optional[str]) -> None:
    """
    If until isn't after since or since is None raise ValidationError
    """
    if since is None:
        raise serializers.ValidationError('"Since cannot be an empty value"')
    if until is None:
        return
    if datetime.datetime.fromisoformat(since) > datetime.datetime.fromisoformat(until):
        raise serializers.ValidationError('"Until" must be after "since"')
