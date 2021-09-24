from typing import Iterable

import factory

from django.contrib.auth import get_user_model


class UserFactory(factory.Factory):
    class Meta:
        model = get_user_model()

    username = factory.Faker("name")
    email = factory.Faker("email")


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "profile.Profile"

    about_me = factory.Faker("text")
    email = factory.Faker("email")
    full_name = factory.Faker("name")
    number = factory.Sequence(lambda n: f'{n}_Number_profile')
    user = factory.SubFactory(UserFactory)
    website = factory.Faker("url")


class ExperienceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "profile.Experience"

    description = factory.Faker("text")
    # TODO : Define DataRangeField
    # experience  = factory.
    employer = factory.Faker("company")
    position = factory.Sequence(lambda n: f'{n}_position')
    user = factory.SubFactory(UserFactory)
