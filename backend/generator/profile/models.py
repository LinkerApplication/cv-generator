from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=150)
    number = models.CharField(max_length=15)
    about_me = models.TextField(blank=True)
    website = models.URLField(blank=True)
    places_of_work = models.ManyToManyField('PlaceOfWork')

    def __str__(self):
        return self.full_name


class PlaceOfWork(models.Model):
    work = models.CharField(max_length=255)
    experience = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'Experience: {self.experience} - Работа: {self.work}'