import datetime

import factory


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'profile.Profile'

    about_me = factory.Faker('text')
    email = factory.Faker('email')
    full_name = factory.Faker('name')
    number = factory.Faker('phone')
    website = factory.Faker('url')


class ExperienceFactory(factory.django.DjangoModelFactory):
    """
    Factory for a separate experience, which belongs to a certain Profile
    Default since date is a fuzzy date between 1.1.1970 and yesterday.
    """
    class Meta:
        model = 'profile.Experience'

    description = factory.Faker('text')
    employer = factory.Faker('company')
    position = factory.Faker('position')
    profile = factory.SubFactory(ProfileFactory)
    since = factory.fuzzy.FuzzyDate(
        datetime.date(1970, 1, 1),
        datetime.date.today() - datetime.timdelta(days=1)
    )
