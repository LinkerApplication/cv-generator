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
    def experience(self, year, month, day):
        date_range = {
            'lower': datetime.date(year, month, day).isoformat(),
            'upper': datetime.time().isoformat()
        }

        return date_range
