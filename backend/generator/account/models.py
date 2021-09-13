from django.db import models


class Profile(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=150)
    number = models.CharField(15)
    about_me = models.TextField()
    website = models.URLField()
    experience = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.full_name
