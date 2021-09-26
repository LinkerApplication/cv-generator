from datetime import datetime, date

import factory

import django.contrib.auth.models as auth_models
from django.db.models.signals import post_save


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "profile.Profile"

    about_me = factory.Faker("text")
    email = factory.Faker("email")
    full_name = factory.Faker("name")
    number = factory.Faker("phone_number")
    user = factory.SubFactory('profile.test.factories.UserFactory', profile=None, null=True)
    website = factory.Faker("url")


@factory.django.mute_signals(post_save)
class UserFactory(factory.Factory):
    class Meta:
        model = auth_models.User

    username = factory.Faker("name")
    email = factory.Faker("email")
    profile = factory.RelatedFactory(ProfileFactory, factory_related_name='user')


class ExperienceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "profile.Experience"

    description = factory.Faker("text")

    @factory.lazy_attribute
    def experience(self, year=2000, month=10, day=10):
        return date(year, month, day).isoformat(), datetime.now().strftime('%Y-%m-%d')

    employer = factory.Faker("company")
    position = factory.Faker("job")
    profile = factory.SubFactory(ProfileFactory)
