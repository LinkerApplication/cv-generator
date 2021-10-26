from rest_framework import serializers


def validate_until_is_after_since(since: str, until: str) -> None:
    if since is None:
        raise serializers.ValidationError('"Since is null"')
    if until is None:
        return
    if since > until:
        raise serializers.ValidationError('"Until" must be more than "since"')
