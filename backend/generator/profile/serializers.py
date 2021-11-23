from rest_framework import serializers

from .models import Experience, Profile
from .validators import validate_until_is_after_since


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ("description", "employer", "position", "since", "until")

    def validate(self, attrs):
        validate_until_is_after_since(attrs.get("since"), attrs.get("until"))
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    experiences = ExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = (
            "email",
            "full_name",
            "number",
            "about_me",
            "website",
            "experiences",
            "pk",
        )
