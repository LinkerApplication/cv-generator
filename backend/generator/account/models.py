from django.db import models


class Profile(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    number = models.CharField(max_length=15)
    about_me = models.TextField(blank=True)
    website = models.URLField(blank=True)
    experience = models.IntegerField(default=0)

    def __str__(self):
        return self.full_name
