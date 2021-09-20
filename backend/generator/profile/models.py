from django.conf import settings
from django.db import models


class Profile(models.Model):
    about_me = models.TextField(blank=True)
    email = models.EmailField(max_length=150)
    full_name = models.CharField(max_length=255)
    number = models.CharField(max_length=15)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    website = models.URLField(blank=True)
    works = models.ManyToManyField('WorksPlace', blank=True)

    def __str__(self):
        return self.full_name


class WorksPlace(models.Model):
    profession = models.CharField(max_length=150)
    experience = models.PositiveSmallIntegerField(max_length=2)
