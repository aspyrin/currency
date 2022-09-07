from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import UserManager
from django.db import models


def user_avatar(instance, filename):
    return 'avatar/{0}/{1}'.format(instance.id, filename)


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField('email address', unique=True)
    avatar = models.FileField(upload_to=user_avatar)
