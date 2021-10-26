from rest_framework import serializers

from .models import Experience, Profile
from .validators import validate_until_is_after_since


class SerializerExperience(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ("description", "experience", "employer", "position", "since", "until")


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="email")
    experiences = SerializerExperience(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = (
            "email",
            "full_name",
            "number",
            "about_me",
            "website",
            "user",
            "since",
            "until",
            "pk",
        )

    def validate(self, attrs):
        validate_until_is_after_since(attrs.get("since"), attrs.get("until"))
