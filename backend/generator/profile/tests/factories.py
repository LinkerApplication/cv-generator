from datetime import datetime, date
from typing import Iterable

import factory

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "profile.Profile"

    about_me = factory.Faker("text")
    email = factory.Faker("email")
    full_name = factory.Faker("name")
    number = factory.Faker("phone_number")
    user = factory.SubFactory('UserFactory', profile=None)
    website = factory.Faker("url")


@factory.django.mute_signals(post_save)
class UserFactory(factory.Factory):
    class Meta:
        model = get_user_model()

    username = factory.Faker("name")
    email = factory.Faker("email")
    profile = factory.RelatedFactory(ProfileFactory, factory_related_name='user')


class ExperienceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "profile.Experience"

    description = factory.Faker("text")

    @factory.lazy_attribute
    def experience(self, year, month, day):
        data_range = (date(year, month, day).isoformat(), datetime.now().strftime('%Y-%m-%d'))
        return data_range

    employer = factory.Faker("company")
    position = factory.Faker("job")
    profile = factory.SubFactory(ProfileFactory)
