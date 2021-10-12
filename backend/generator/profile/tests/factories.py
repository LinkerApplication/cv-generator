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
    class Meta:
        model = 'profile.Experience'

    description = factory.Faker('text')
    employer = factory.Faker('company')
    position = factory.Faker('position')
    profile = factory.SubFactory(ProfileFactory)

    @factory.lazy_attribute
    def lower(self, year, month, day):
        return datetime.date(year, month, day).isoformat()

    @factory.lazy_attribute
    def upper(self, year, month, day):
        return datetime.date(year, month, day).isoformat()
