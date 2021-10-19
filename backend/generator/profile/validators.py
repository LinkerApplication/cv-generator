from rest_framework import serializers


def check_that_until_more_than_until(since: str, until: str) -> None:
    if since >= until:
        raise serializers.ValidationError('"Until" must be more than "since"')
