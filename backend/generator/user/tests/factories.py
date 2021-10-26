import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.Factory):
    class Meta:
        model = get_user_model()

    email = factory.Faker("email")