"""
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from .models import CustomUser
from .tokens import account_activation_token  

@receiver(post_save, sender=CustomUser)
def send_verification_email(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        # Use the site's domain from settings if you don't have an HttpRequest
        domain = getattr(settings, 'SITE_DOMAIN', 'example.com')
        mail_subject = 'Activate your account'
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        token = account_activation_token.make_token(instance)
        verification_url = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        message = render_to_string('account_verification_email.html', {
            'user': instance,
            'domain': domain,  # Replace with the domain directly
            'uid': uid,
            'token': token,
            'verification_url': f'{domain}{verification_url}'  # Include the full URL
        })
        to_email = instance.email

        # Use EmailMultiAlternatives to send both plain text and HTML
        email = EmailMultiAlternatives(
            subject=mail_subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email]
        )
        email.attach_alternative(message, "text/html")  # Specify that this is an HTML message
        email.send()
"""