from django.db import models
from .manager import CustomUserManager
from base.models import BaseModel
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from .tokens import account_activation_token
import random
from django.urls import reverse

# Create your models here.
class CustomUser(BaseModel, AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True
    )

    def __str__(self) -> str:
        return f'{self.email}'


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    contact = models.CharField(max_length=30, unique=True, null=True, blank=True)
    address = models.CharField(max_length=200)
    ntn = models.CharField(max_length=10, unique=True, null=True, blank=True)

    REQUIRED_FIELDS = ['contact']

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)  # Create UserProfile instance


@receiver(post_save, sender=CustomUser)
def send_verification_email(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        # Prepare to send the email
        domain = getattr(settings, 'SITE_DOMAIN', 'example.com')
        mail_subject = 'Activate your account'
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        token = account_activation_token.make_token(instance)
        verification_url = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        
        message = render_to_string('users/account_verification_email.html', {
            'user': instance,
            'domain': domain,
            'uid': uid,
            'token': token,
            'verification_url': f'{domain}{verification_url}'
        })
        to_email = instance.email

        # Send the email
        email = EmailMultiAlternatives(
            subject=mail_subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email]
        )
        email.attach_alternative(message, "text/html")
        email.send()
