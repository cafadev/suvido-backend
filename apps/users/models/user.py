from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager
from apps.common.base import BaseModel


class User(BaseModel, AbstractBaseUser, PermissionsMixin):

    username = None
    start_date = None
    date_joined = None

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    image = models.ImageField(upload_to='profiles', null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email