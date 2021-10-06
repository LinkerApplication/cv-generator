from rest_framework import serializers
from drf_extra_fields.fields import DateRangeField

from .models import Profile, Experience


class SerializerCreateExperience(serializers.ModelSerializer):
    experience = DateRangeField()

    class Meta:
        model = Experience
        fields = (
             'description', 'experience',
             'employer', 'position',
        )


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='email')
    experiences = SerializerCreateExperience(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = (
            'email', 'full_name',
            'number', 'about_me',
            'website', 'user',
            'experiences',
            'pk',
        )
