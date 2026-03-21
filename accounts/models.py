from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin, UserManager

class User(AbstractUser):

    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username