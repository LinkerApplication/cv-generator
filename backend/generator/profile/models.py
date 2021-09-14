from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=150)
    number = models.CharField(max_length=15)
    about_me = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.full_name
