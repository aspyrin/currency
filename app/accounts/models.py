from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField('email address', unique=True)