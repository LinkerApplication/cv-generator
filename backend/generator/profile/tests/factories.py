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
    Factory of Experience and subFactory of Profile
    
    @param description: str
    @param employer: str
    @param position: str
    @param profile: ProfileFactory
    """
    class Meta:
        model = 'profile.Experience'

    description = factory.Faker('text')
    employer = factory.Faker('company')
    position = factory.Faker('position')
    profile = factory.SubFactory(ProfileFactory)

    @factory.lazy_attribute
    def since(self, year: int, month: int, day: int):
        """
        Creating date for field 'since'
        """ 
        return datetime.date(year, month, day).isoformat()

    @factory.lazy_attribute
    def until(self, year: int, month: int, day: int):
        """
        Creating date for field 'until'
        """
        return datetime.date(year, month, day).isoformat()
