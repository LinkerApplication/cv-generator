import datetime

import factory
from factory.fuzzy import FuzzyDate


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "profile.Profile"

    about_me = factory.Faker("text")
    email = factory.Faker("email")
    full_name = factory.Faker("name")
    number = factory.Faker("phone_number")
    website = factory.Faker("url")


class ExperienceFactory(factory.django.DjangoModelFactory):
    """
    Factory for a separate experience, which belongs to a certain Profile
    Default since date is a fuzzy date between 1.1.1970 and yesterday.
    """

    class Meta:
        model = "profile.Experience"

    description = factory.Faker("text")
    employer = factory.Faker("company")
    position = factory.Faker("job")
    profile = factory.SubFactory(ProfileFactory)
    since = factory.Faker('date_object')
