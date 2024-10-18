from django.db import models
from .manager import CustomUserManager
from base.models import BaseModel
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class CustomUser(BaseModel, AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Set a custom related name to avoid clash with auth.User.groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Set a custom related name to avoid clash with auth.User.user_permissions
        blank=True
    )


    def __str__(self) -> str:
        return f'self.email'
    
"""
class UserProfile(models.Model):
    contact = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=200)
    ntn = models.CharField(max_length=10, unique=True)

    REQUIRED_FIELDS = ['contact']
"""