from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: List[str] = []

    objects = UserManager()

    def __str__(self):
        return self.email
