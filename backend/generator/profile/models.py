from django.conf import settings
from django.contrib.postgres.fields import DateRangeField
from django.db import models


class Profile(models.Model):
    about_me = models.TextField(blank=True)
    email = models.EmailField(max_length=150)
    full_name = models.CharField(max_length=255)
    number = models.CharField(max_length=15)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.full_name


class Experience(models.Model):
    description = models.TextField(max_length=2000)
    experience = DateRangeField()
    employer = models.CharField(max_length=255)
    position = models.CharField(max_length=150)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')

    def __str__(self):
        return f'{self.profile.full_name}: {self.employer}'
